import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideHttpClient } from '@angular/common/http';

/**
 * Core configuration for the Angular application.
 * Sets up essential providers for routing, HTTP, and change detection.
 * 
 * @type {ApplicationConfig}
 * 
 * @description
 * Configures the application with:
 * - Zone.js change detection with event coalescing
 * - Router configuration using defined routes
 * - HTTP client for making API requests
 */
export const appConfig: ApplicationConfig = {
  /**
   * Core application providers array
   * @property {Function} provideZoneChangeDetection - Configures Zone.js change detection
   * @property {Object} eventCoalescing - Enables batching of multiple change detection runs
   * @property {Function} provideRouter - Sets up routing using defined routes
   * @property {Function} provideHttpClient - Enables HTTP capabilities
   */
  providers: [
      provideZoneChangeDetection({ eventCoalescing: true }),  // Optimizes change detection
      provideRouter(routes),                                  // Sets up routing
      provideHttpClient()                                     // Enables HTTP requests
  ]
};
