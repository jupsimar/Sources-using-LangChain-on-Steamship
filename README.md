# Overview
This is a Replit example of a Question Answering app built with [LangChain](https://langchain.readthedocs.io/en/latest/) (🦜️🔗) and deployed on [Steamship](https://steamship.com).

Steamship is the fastest way to build, ship, and use full-lifecycle language AI.

By deploying on Steamship, LangChain developers get:

- Production-ready API endpoint(s)
- Horizontal scaling across dependencies / backends
- Persistent storage of app state (including caches)
- Built-in support for Authn/z 
- Multi-tenancy support
- Seamless integration with other Steamship skills (ex: audio transcription) 
- Usage Metrics and Logging
- And much more...

The GitHub repo for the LangChain adapters for Steamship is: https://github.com/steamship-core/steamship-langchain

## Quick Start

To run it locally:
1. Get a Steamship API Key (Visit: [https://steamship.com/account/api](https://www.steamship.com/account/api)). If you do not
   already have a Steamship account, you will need to create one.
1. Copy this key to a [Replit Secret](https://docs.replit.com/programming-ide/storing-sensitive-information-environment-variables) named `STEAMSHIP_API_KEY`.
1. Click the green `Run` button at the top of the window (or open a new Shell and type `python3 api.py`).

If you want to get a production API endpoint for your app, type `ship deploy` in a Shell.

# Question Answering API

## Prerequisites

You will need a [Steamship](https://steamship.com) Account and an associated API Key. With an account, an API Key can be obtained
via the website ([https://www.steamship.com/account/api](https://www.steamship.com/account/api)).

You will need to create a Replit Secret for `STEAMSHIP_API_KEY` with your Steamship API key. 

## Local test/development

To run the package locally, use the provided `Run` button in Replit (or open a new Shell and type `python3 api.py`).

## Production deployment

Once you are satisfied with your app, you may deploy it to Steamship in order to create running production-ready instance(s).

To deploy it on [Steamship](https://steamship.com), open a **new** Shell and type `ship deploy`. This will push a new version of your Steamship package to Steamship's servers.

Details about the package will be accessible via https://www.steamship.com/packages/<your-package-name\>.

# Package Files

## `api.py`

The main logic for the generator lives entirely in `api.py`. All Steamship packages MUST have an api.py file.

## `steamship.json`

After you deploy once, you will see a new `steamship.json` file in your repl. This is the manifest Steamship uses to store metadata about your package. This includes a handle for the package, as well as a version (allowing for package updates). This information will be used when you deploy your package to Steamship to present package details to users.

## `requirements.txt`

This file is used by [Steamship](https://steamship.com) in the package deployment process. Any dependencies that are needed by your code should be added here to ensure they are accessible to your package at runtime.

# About Steamship

[Steamship](https://steamship.com) is the fastest way to deploy language AI.

Steamship [packages](https://steamship.com/packages) provide a mechanism for encapsulating and deploying your language AI logic, 
allowing invocation with parameters that supports auto-scaling and persistence via a static HTTP endpoint.

Steamship packages can combine multiple Steamship [plugins](https://steamship.com/plugins) to build complex applications out of various AI building blocks. These plugins cover a broad variety of AI skills, including transcription, summarization, and generation.

To learn more about Steamship packages and plugins, please read our docs: https://docs.steamship.com/.
