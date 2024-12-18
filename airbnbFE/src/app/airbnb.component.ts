import { Component } from '@angular/core';
import { RouterOutlet, RouterModule } from '@angular/router';
import { DataService } from './data.service';
import { WebService } from './web.service';

/**
 * Component for displaying and managing paginated property listings.
 * Handles data fetching, page navigation, and session storage for page persistence.
 * 
 * @class ListingsComponent
 * @implements {Component}
 * 
 * @description
 * Provides functionality for:
 * - Displaying property listings
 * - Pagination controls
 * - Session-based page persistence
 * - Data fetching from WebService
 */
@Component({
    selector: 'listings',
    imports: [RouterOutlet, RouterModule],
    providers: [DataService, WebService],
    templateUrl: './airbnb.component.html',
    styleUrl: './airbnb.component.css'
})
export class ListingsComponent {
    /** Current list of property listings */
    listings_list: any;

    /** Current page number, defaults to 1 */
    page: number = 1;

    /**
     * Creates an instance of ListingsComponent.
     * 
     * @constructor
     * @param {DataService} dataService - Service for utility data operations
     * @param {WebService} webService - Service for fetching listing data
     */
    constructor(public dataService: DataService, public webService: WebService) { }

    /**
     * Lifecycle hook that runs on component initialization.
     * Restores the page number from session storage if available
     * and fetches the initial set of listings.
     * 
     * @method ngOnInit
     */
    ngOnInit() {
        if (sessionStorage['page']) {
            this.page = Number(sessionStorage['page']);
        }
        
        this.webService.getListings(this.page)
            .subscribe((response) => {
                this.listings_list = response;
            });
    }

    /**
     * Navigates to the previous page of listings if available.
     * Updates session storage and fetches new listings data.
     * 
     * @method previousPage
     */
    previousPage() {
        if (this.page > 1) {
            this.page = this.page - 1;
            sessionStorage['page'] = this.page;
            this.webService.getListings(this.page).subscribe((response: any) => {
                this.listings_list = response;
            });
        }
    }

    /**
     * Navigates to the next page of listings if available.
     * Updates session storage and fetches new listings data.
     * 
     * @method nextPage
     */
    nextPage() {
        if (this.page < this.webService.getLastPageNumber()) {
            this.page = this.page + 1;
            sessionStorage['page'] = this.page;
            this.webService.getListings(this.page).subscribe((response: any) => {
                this.listings_list = response;
            });
        }
    }
}
