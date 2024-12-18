import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { WebService } from './web.service';
import { AgGridAngular } from 'ag-grid-angular';
import { 
    ColDef, 
    ClientSideRowModelModule, 
    ValidationModule, 
    TextFilterModule, 
    NumberFilterModule,
    PaginationModule,
    HighlightChangesModule
} from 'ag-grid-community';
import { CommonModule } from '@angular/common';

/**
 * Grid component that displays listing data using AG Grid.
 * Provides features like pagination, filtering, and animated cell changes.
 * 
 * @class GridComponent
 * @implements {Component}
 * 
 * @description
 * this implements the AG Grid to display property listings data with:
 * - Column filtering
 * - Floating filters
 * - Pagination
 * - Animated cell changes
 * - Responsive design
 */
@Component({
    selector: 'grid',
    standalone: true,
    imports: [RouterOutlet, AgGridAngular, CommonModule],
    providers: [WebService],
    templateUrl: './grid.component.html',
    styleUrl: './grid.component.css'
})
export class GridComponent {
    /**
     * Column definitions for AG Grid.
     * Configures the display and behavior of each column in the grid.
     * 
     * @type {ColDef[]}
     * @property {string} field - The data field to display
     * @property {boolean} filter - Whether filtering is enabled
     * @property {boolean} floatingFilter - Whether to show filter input in header
     */
    headings: ColDef[] = [
        { field: "name" },
        { field: "accommodates", filter: true, floatingFilter: true },
        { field: "bedrooms", filter: true, floatingFilter: true },
        { field: "bathrooms", filter: true, floatingFilter: true },
        { field: "price", filter: true, floatingFilter: true },
        { 
            field: 'review_scores_rating', 
            headerName: 'Rating', 
            filter: true, 
            floatingFilter: true, 
            cellRenderer: 'agAnimateShowChangeCellRenderer', 
            cellRendererParams: { flashDelay: 1000 }
        },
    ];

    /** Array to store the grid data fetched from the web service */
    data: any = [];

    /**
     * AG Grid modules required for grid functionality.
     * @type {Array}
     */
    modules = [
        ClientSideRowModelModule, 
        ValidationModule, 
        TextFilterModule, 
        NumberFilterModule,
        PaginationModule,
        HighlightChangesModule
    ]; 

    /** Enable grid pagination */
    pagination = true;

    /** Number of rows per page */
    paginationPageSize = 10;

    /** Available options for rows per page */
    paginationPageSizeSelector = [10, 25, 50, 100];

    /**
     * Creates an instance of GridComponent.
     * @constructor
     * @param {WebService} webService - Service for fetching listing data
     */
    constructor(private webService: WebService) { }

    /**
     * Lifecycle hook that runs after component initialization.
     * Fetches all listings data from the web service.
     * 
     * @method ngOnInit
     * @memberof GridComponent
     */
    ngOnInit() {
        this.webService.getAllListings()
            .subscribe((response) => {
                this.data = response;
            });
    }
}