import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


export interface PriceRangeSummary {
    range: string;
    min: number;
    max: number | null;
    count: number;
    percentage: number;
    listings: {
        id: string;
        name: string;
        price: string;
    }[];
}

export interface PriceRangeResponse {
    data: PriceRangeSummary[];
    total_listings: number;
}

/**
 * Service responsible for handling all HTTP communications with the listings API.
 * Provides methods for CRUD operations on listings and reviews.
 * @class WebService
 * @injectable
 */
@Injectable()
export class WebService {
    /** Number of items to display per page */
    pageSize: number = 6;
    
    /** Total number of listings in the database */
    private totalListings: number = 0;

    /**
     * Creates an instance of WebService and initializes total listings count.
     * @constructor
     * @param {HttpClient} http - The Angular HTTP client for making API requests
     */
    constructor(private http: HttpClient) {
        this.getAllListings().subscribe(response => {
            this.totalListings = response.length;
        });
    }

    /**
     * Retrieves a paginated list of listings.
     * @param {number} page - The page number to retrieve
     * @returns {Observable<any>} Observable containing the paginated listings
     */
    getListings(page: number) {
        return this.http.get<any>(
            'http://127.0.0.1:5000/api/v1.0/listings?pn=' + page + '&ps=' + this.pageSize
        );
    }

    /**
     * Retrieves a specific listing by ID.
     * @param {any} id - The ID of the listing to retrieve
     * @returns {Observable<any>} Observable containing the listing details
     */
    getListing(id: any) {
        return this.http.get<any>(
            'http://127.0.0.1:5000/api/v1.0/listings/' + id);
    }

    /**
     * Posts a new review for a specific listing.
     * @param {any} id - The ID of the listing to review
     * @param {Object} review - The review details
     * @param {string} review.user_name - Name of the reviewer
     * @param {string} review.comments - Review content
     * @param {string} review.date - Date of the review
     * @returns {Observable<any>} Observable containing the created review
     */
    postReview(id: any, review: any) {
        let postData = new FormData();
        postData.append('user_name', review.user_name);
        postData.append('comments', review.comments);
        postData.append('date', review.date);
        return this.http.post<any>('http://127.0.0.1:5000/api/v1.0/listings/' + id + '/reviews', postData);
    }

    /**
     * Retrieves all reviews for a specific listing.
     * @param {any} id - The ID of the listing to get reviews for
     * @returns {Observable<any>} Observable containing the listing's reviews
     */
    getReviews(id: any) {
        return this.http.get<any>('http://127.0.0.1:5000/api/v1.0/listings/' + id + '/reviews');
    }

    /**
     * Retrieves all listings without pagination.
     * @returns {Observable<any>} Observable containing all listings
     */
    getAllListings() {
        return this.http.get<any>(
            'http://127.0.0.1:5000/api/v1.0/listings?pn=1&ps=3000');
    }

    /**
     * Updates an existing listing.
     * @param {string} id - The ID of the listing to update
     * @param {Object} listing - The updated listing details
     * @param {string} listing.name - Name of the property
     * @param {string} listing.description - Property description
     * @param {string} listing.property_type - Type of property
     * @param {string} listing.room_type - Type of room
     * @param {number} listing.accomodates - Number of guests that can be accommodated
     * @param {number} listing.bathrooms - Number of bathrooms
     * @param {number} listing.bedrooms - Number of bedrooms
     * @param {number} listing.beds - Number of beds
     * @param {string} listing.amenities - Available amenities
     * @param {number} listing.price - Price per night
     * @param {number} listing.minimum_nights - Minimum stay duration
     * @param {number} listing.maximum_nights - Maximum stay duration
     * @param {number} listing.review_scores_rating - Overall review score
     * @param {number} listing.review_scores_location - Location review score
     * @param {string} listing.neighbourhood - Property neighborhood
     * @returns {Observable<any>} Observable containing the updated listing
     */
    updateListing(id: string, listing: any) {
        let postData = new FormData();
        postData.append('name', listing.name);
        postData.append('description', listing.description);
        postData.append('property_type', listing.property_type);
        postData.append('room_type', listing.room_type);
        postData.append('accomodates', listing.accomodates);
        postData.append('bathrooms', listing.bathrooms);
        postData.append('bedrooms', listing.bedrooms);
        postData.append('beds', listing.beds);
        postData.append('amenities', listing.amenities);
        postData.append('price', listing.price);
        postData.append('minimum_nights', listing.minimum_nights);
        postData.append('maximum_nights', listing.maximum_nights);
        postData.append('review_scores_rating', listing.review_scores_rating);
        postData.append('review_scores_location', listing.review_scores_location);
        postData.append('neighbourhood', listing.neighbourhood);

        return this.http.put<any>('http://127.0.0.1:5000/api/v1.0/listings/' + id, postData);
    }

    /**
     * Deletes a specific listing.
     * @param {string} id - The ID of the listing to delete
     * @returns {Observable<any>} Observable containing the deletion response
     */
    deleteListing(id: string) {
        return this.http.delete<any>('http://127.0.0.1:5000/api/v1.0/listings/' + id);
    }

    /**
     * Calculates the total number of pages based on total listings and page size.
     * @returns {number} The last page number
     */
    getLastPageNumber() {
        return Math.ceil(this.totalListings / this.pageSize);
    }

    /**
     * Retrieves price range summary for all listings
     * @returns {Observable<PriceRangeResponse>} Observable containing the price range summary
     */
    getPriceRangeSummary() {
        return this.http.get<PriceRangeResponse>(
            'http://127.0.0.1:5000/api/v1.0/listings/priceRangeSummary'
        );
    }
}