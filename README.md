# Docker Compose Templates for Portainer Stacks

![](qube_logo_website.png)

This repository contains a set of Docker Compose files designed to be used as templates for deploying services in Portainer. These templates provide an easy and flexible way to set up various stacks, allowing you to quickly deploy common services and applications using Portainer's stack management.

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Portainer allows users to manage Docker environments, including the deployment of stacks using Docker Compose files. This repository serves as a library of ready-to-use Docker Compose files that can be directly imported into Portainer to deploy commonly used services and configurations.

## Prerequisites

Before using these templates, ensure that:
- You have Docker and Docker Compose installed on your server.
- Portainer is installed and accessible. You can learn more about setting up Portainer [here](https://www.portainer.io/installation).

## Usage

To use these templates in Portainer:

1. Open Portainer and navigate to the **Stacks** section.
2. Click on **Add Stack** to create a new stack.
3. In the **Web editor** section, choose the **Repository** method for importing a stack.
4. Enter the GitHub URL of this repository:
    ```text
    https://github.com/your-username/docker-compose-templates
    ```
5. Select the Docker Compose file you wish to deploy from the dropdown.
6. Customize environment variables or other options as needed.
7. Click **Deploy the stack** to start the service.

Portainer will pull the selected Compose file directly from the GitHub repository and deploy the stack.

## Contributing

Contributions are welcome! If you have a useful stack template that you'd like to add, feel free to open a pull request. Please ensure your submission follows the same formatting and structure as the existing templates.

## License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

