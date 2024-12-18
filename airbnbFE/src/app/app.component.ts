import { Component } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';
import { ListingsComponent } from './airbnb.component';
import { NavComponent } from './nav.component';
import { DataService } from './data.service';
import { GridComponent } from './grid.component';
import { WebService } from './web.service';


/**
 * Root component of the Airbnb application.
 * Acts as the main container and bootstrapping component.
 * 
 * @class AppComponent
 * @implements {Component}
 * 
 * @description
 * A standalone component that:
 * - Serves as the application shell
 * - Provides core services to child components
 * - Manages routing and navigation
 * - Integrates essential components like Navigation and Listings
 * 
 * @example
 * <!-- Usage in index.html -->
 * <app-root></app-root>
 */
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
      RouterOutlet,        // For routing support
      ListingsComponent,   // Property listings component
      NavComponent,        // Navigation component
      GridComponent,       // Grid view component
      RouterModule        // Angular router functionality
  ],
  providers: [
      DataService,        // Utility data service
      WebService         // Main web API service
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  /** Title of the application */
  title = 'Airbnb';

  /**
   * Creates an instance of AppComponent.
   * 
   * @constructor
   * @param {DataService} dataService - Service for utility data operations
   */
  constructor(private dataService: DataService) {}
}
