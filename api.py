"""A Steamship package for answering questions with sources using Embeddings and LangChain.

To run it:
1. Get a Steamship API Key (Visit: https://steamship.com/account/api). If you do not
   already have a Steamship account, you will need to create one.
2. Copy this key to a Replit Secret named STEAMSHIP_API_KEY.
3. Click the green `Run` button at the top of the window (or open a Shell and type `python3 api.py`).

To see additional Steamship + Langchain examples, please visit our GitHub repo:
https://github.com/steamship-core/steamship-langchain

More information is provided in README.md.

To learn more about advanced uses of Steamship, read our docs at: https://docs.steamship.com/packages/using.html.
"""
import logging
from typing import Any, Dict, List

import langchain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from steamship import Block, check_environment, File, RuntimeEnvironments, Steamship, Tag
from steamship.data.plugin.index_plugin_instance import SearchResult
from steamship.invocable import post, PackageService
from steamship_langchain.cache import SteamshipCache
from steamship_langchain.llms import OpenAI
from termcolor import colored


class QuestionAnsweringPackage(PackageService):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    # set up LLM cache
    langchain.llm_cache = SteamshipCache(self.client)
    # set up LLM
    self.llm = OpenAI(client=self.client,
                      temperature=0,
                      cache=False,
                      max_words=250)
    # create a persistent embedding store
    self.index = self.client.use_plugin(
      "embedding-index",
      config={
        "embedder": {
          "plugin_handle": "openai-embedder",
          "fetch_if_exists": True,
          "config": {
            "model": "text-embedding-ada-002",
            "dimensionality": 1536,
          }
        }
      },
      fetch_if_exists=True,
    )

  @post("index_file")
  def index_file(self, file_handle: str) -> bool:
    text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=0)
    texts = []
    file = File.get(self.client, handle=file_handle)
    for block in file.blocks:
      texts.extend(text_splitter.split_text(block.text))

    # give an approximate source location based on chunk size
    items = [
      Tag(client=self.client,
          text=t,
          value={"source": f"{file.handle}-offset-{i*250}"})
      for i, t in enumerate(texts)
    ]

    self.index.insert(items)
    return True

  @post("search_embeddings")
  def search_embeddings(self, query: str, k: int) -> List[SearchResult]:
    """Return the `k` closest items in the embedding index."""
    search_results = self.index.search(query, k=k)
    search_results.wait()
    items = search_results.output.items
    return items

  @post("/qa_with_sources")
  def qa_with_sources(self, query: str) -> Dict[str, Any]:
    chain = load_qa_with_sources_chain(self.llm,
                                       chain_type="map_reduce",
                                       verbose=False)
    search_results = self.search_embeddings(query, k=4)
    docs = [
      Document(page_content=result.tag.text,
               metadata={"source": result.tag.value.get("source", "unknown")})
      for result in search_results
    ]
    return chain({"input_documents": docs, "question": query})


# Try it out locally by running this file!
if __name__ == "__main__":
  logging.getLogger().setLevel(logging.ERROR)
  print(
    colored("Question Answering with Sources using LangChain on Steamship\n",
            attrs=['bold']))

  # This helper provides runtime API key prompting, etc.
  check_environment(RuntimeEnvironments.REPLIT)

  # NOTE: we use a temporary workspace here as an example.
  # To persist chat history across sessions, etc., use a persistent workspace.
  with Steamship.temporary_workspace() as client:
    # when ...
    api = QuestionAnsweringPackage(client=client)

    # Embed the State of the Union address
    with open("state-of-the-union-2022.txt") as f:
      print(colored(
        "Saving the state of the union file to Steamship workspace...",
        "blue"),
            end="",
            flush=True)
      sotu_file = File.create(client, blocks=[Block(text=f.read())])
      print(colored("Done.", "blue"))

    print(colored("Indexing state of the union...", "blue"),
          end="",
          flush=True)
    # when ...
    api.index_file(file_handle=sotu_file.handle)
    print(colored("Done.", "blue"))

    # Issue Query
    query = "tell me about Canada?"
    print(colored("\nQuery: ", "blue"), f"{query}")

    print(
      colored(
        "Awaiting results. Please be patient. This may take a few moments.",
        "blue"))

    # when...
    response = api.qa_with_sources(query=query)
    print(colored("Answer: ", "blue"), f"{response['output_text'].strip()}")

    # Print sources (with text)
    last_line = response['output_text'].splitlines()[-1:][0]

    if "SOURCES: " not in last_line:
      print(colored("No sources provided in response.", "red"))
    else:
      sources_list = last_line[len("SOURCES: "):]

      for source in sources_list.split(","):
        print(colored(f"\nSource text ({source.strip()}):", "blue"))
        for input_doc in response['input_documents']:
          metadata = input_doc.metadata
          src = metadata['source']
          if source.strip() == src:
            print(input_doc.page_content)
