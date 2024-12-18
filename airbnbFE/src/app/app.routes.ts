import { Routes } from '@angular/router';
import { HomeComponent } from './home.component';
import { ListingsComponent } from './airbnb.component';
import { ListingComponent } from './listing.component';
import { GridComponent } from './grid.component';

/**
 * Main routing configuration for the application.
 * Defines the available routes and their corresponding components.
 * 
 * @type {Routes}
 * 
 * @description
 * Route structure:
 * - '/' -> Home page
 * - '/listings' -> List of all properties
 * - '/listings/:id' -> Individual property details
 * - '/grid' -> Grid view of properties
 */
export const routes: Routes = [
    /**
     * Default route - Home page
     * @path ''
     * @component HomeComponent
     */
    {
        path: '',
        component: HomeComponent
    },

    /**
     * Listings route - Displays all property listings
     * @path 'listings'
     * @component ListingsComponent
     */
    {
        path: 'listings',
        component: ListingsComponent
    }, 

    /**
     * Individual listing route - Shows detailed view of a specific property
     * @path 'listings/:id'
     * @component ListingComponent
     * @param {string} id - The unique identifier of the listing
     */
    {
        path: 'listings/:id',
        component: ListingComponent
    },

    /**
     * Grid route - Displays properties in a grid layout
     * @path 'grid'
     * @component GridComponent
     */
    {
        path: 'grid',
        component: GridComponent
    }
];
