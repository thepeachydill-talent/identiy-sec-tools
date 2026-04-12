# identiy-sec-tools
home lab for IAM integration with Google Workspace
## Identity Security Lab

This project is a personal lab environment for exploring **Identity and Access Management (IAM)** concepts and implementations.

It simulates a modern identity architecture using an external identity provider and a relying application to demonstrate authentication, authorization, and identity-driven access control patterns.

The goal is to progressively build a working identity security environment that models real-world enterprise IAM workflows such as:

- Federated authentication
- Role-based access control (RBAC)
- Identity lifecycle automation
- Privileged access management concepts
- SaaS access governance

# Current Implementation

The project currently demonstrates a working **OpenID Connect authentication flow** between a Flask application and a Keycloak identity provider.

## Identity Provider

A local Keycloak instance is configured as the identity provider.

Current configuration includes:

- Created a realm for the lab environment
- Registered an OpenID Connect client for the Flask application
- Configured client credentials and redirect URIs
- Enabled OpenID Connect authentication flow

## Application (Flask)

A Python Flask application acts as the relying party for authentication.

The following functionality has been implemented:

- OpenID Connect discovery using the Keycloak metadata endpoint
- Redirecting users to the identity provider for authentication
- Authorization code exchange for tokens
- Validation of returned identity tokens
- Session creation after successful authentication
- Retrieval of user identity claims from the token

Once authenticated, the application displays the logged-in user.

Example output:
hello

## Identity Claims Retrieved

The application currently retrieves the following claims from the ID token:

- `preferred_username`
- `email`
- `given_name`
- `family_name`
- `name`
- `issuer`
- `audience`
- token timestamps

These claims are extracted from the OpenID Connect ID token returned during authentication.

## Identity Lifecycle Automation
This project includes basic identity lifecycle automation using the Keycloak Admin API. These scripts simulate common IAM workflows such as user provisioning, role assignment, and deprovisioning.

All automations are implemented in Python and interact directly with Keycloak to manage users and roles within the configured realm.

### Components
- create user (provisions new user with req. credentials)
- assign role (grants access based on spec. role)
- disable user (revokes access by disabling acct.)

### Implementation 
Lifecycle Oerations are built using KeyCloak Admin API in the scripts in this repo. 

## Technologies Used

- **Keycloak** — Identity Provider
- **Flask** — Web application framework
- **Authlib** — OpenID Connect client library
- **python-dotenv** — Environment configuration
- **requests** — HTTP client library

## Authentication Flow
User
↓
Flask Application
↓
Redirect to Keycloak login
↓
User authenticates
↓
Authorization code returned to Flask
↓
Token exchange
↓
User session created
↓
Authenticated application access

# Work In Progress

The current implementation focuses on authentication.

Future development will expand the lab to demonstrate authorization and identity governance capabilities.

Planned updates include:

- Just-In-Time privileged access concepts
- Integration with SaaS platforms (e.g., Google Workspace)
- Audit logging and access tracking


## Current Status
Current milestone:
- ✔ OIDC authentication successfully implemented
- ✔ Token exchange functioning
- ✔ User identity claims retrieved
- ✔ Session-based authentication working
- ➡ Implement role-based authorization

Next milestone:
- Just-In-Time Implementation
- SaaS Integration
- Audit logging/tacking

# Project Purpose

This lab explores how identity providers integrate with applications and how identity becomes the central control plane for access management in modern architectures.