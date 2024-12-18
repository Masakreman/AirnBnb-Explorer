/**
 * Main entry point for bootstrapping the Angular application.
 * Configures Auth0 authentication and core providers.
 * 
 * @file main.ts
 * @description
 * This file:
 * - Bootstraps the root AppComponent
 * - Sets up Auth0 authentication
 * - Configures HTTP client
 * - Applies core application providers
 * - Handles bootstrap errors
 */

import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';
import { provideAuth0 } from '@auth0/auth0-angular';
import { provideHttpClient } from '@angular/common/http';

/**
 * Bootstraps the application with required providers and configuration.
 * 
 * @function bootstrapApplication
 * @param {Type<AppComponent>} AppComponent - The root component of the application
 * @param {ApplicationConfig} config - Configuration object containing providers
 * 
 * @example
 * The application is bootstrapped with:
 * - Auth0 configuration for authentication
 * - HTTP client for API requests
 * - Core application providers from appConfig
 */
bootstrapApplication(AppComponent, {
  providers: [
    // Auth0 provider configuration
    provideAuth0({
      domain: 'dev-e0wg4rv17ljv4b74.us.auth0.com',
      clientId: 'y25qZ8qHUwdjbSespAtSTkpLi1Z0FDii',
      authorizationParams: {
        redirect_uri: window.location.origin
      }
    }),
    // HTTP client provider for API requests
    provideHttpClient(),
    // Core application providers
    appConfig.providers
  ]
}).catch((err) => console.error(err));