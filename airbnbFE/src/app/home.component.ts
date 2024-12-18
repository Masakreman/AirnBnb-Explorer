/**
 * @file home.component.ts
 * @description This file defines the `HomeComponent`, which displays a summary of listing price ranges, 
 *              including a distribution of prices and an option to view individual listings within each range.
 *              It fetches data from a `WebService` and manages loading and error states.
 */

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WebService } from './web.service';

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    standalone: true,
    imports: [CommonModule]
})
export class HomeComponent implements OnInit {
    /**
     * @property {Array<any>} priceRanges - Array of price range objects containing the range, count, percentage, 
     *                                      and listings for each range.
     */
    priceRanges: any[] = [];

    /**
     * @property {boolean} loading - Indicates whether the component is currently fetching data.
     */
    loading = false;

    /**
     * @property {boolean} error - Indicates whether there was an error fetching data.
     */
    error = false;

    /**
     * @constructor
     * @param {WebService} webService - The service used to fetch price range summary data from the backend.
     */
    constructor(private webService: WebService) {}

    /**
     * Lifecycle hook called when the component is initialized.
     * Initiates the data fetching process for the price range summary.
     * 
     * @returns {void}
     */
    ngOnInit(): void {
        this.fetchPriceRangeSummary();
    }

    /**
     * Fetches the price range summary data from the backend.
     * Populates the `priceRanges` array and handles loading and error states.
     * Each price range object in the response is extended with a `showListings` property 
     * to toggle the display of individual listings.
     * 
     * @private
     * @returns {void}
     */
    private fetchPriceRangeSummary(): void {
        this.loading = true;
        this.webService.getPriceRangeSummary().subscribe({
            next: (response) => {
                this.priceRanges = response.data.map(range => ({
                    ...range,
                    showListings: false
                }));
                this.loading = false;
            },
            error: (error) => {
                console.error('Error fetching price range summary:', error);
                this.error = true;
                this.loading = false;
            }
        });
    }
}
