import { Component } from '@angular/core';
import { RouterOutlet, ActivatedRoute, Router } from '@angular/router';
import { DataService } from './data.service';
import { CommonModule } from '@angular/common';
import { GoogleMapsModule } from '@angular/google-maps';
import { Form, ReactiveFormsModule } from '@angular/forms';
import { FormBuilder, Validators } from '@angular/forms'
import { AuthService } from '@auth0/auth0-angular';
import { WebService } from './web.service';

/**
 * Component representing a listing with its details, reviews, and related functionalities.
 */
@Component({
    selector: 'listing',
    standalone: true,
    imports: [RouterOutlet, CommonModule, GoogleMapsModule, ReactiveFormsModule],
    providers: [DataService, WebService],
    templateUrl: './listing.component.html',
    styleUrls: ['./listing.component.css']
})
export class ListingComponent {
    listing_list: any;
    review_list: any;
    listing_lat: any;
    listing_lng: any;
    map_options: google.maps.MapOptions = {};
    map_locations: any[] = [];
    loremIpsum: any;
    temperature: any;
    weather: any;
    weatherIcon: any;
    weatherIconURL: any;
    temperatureColour: any;
    reviewForm: any;
    editForm: any;
    isEditing: boolean = false;
    Math = Math;

    /**
     * Initializes the component with necessary services.
     * @param dataService Service for data operations.
     * @param route Activated route to get route parameters.
     * @param router Router for navigation.
     * @param formBuilder Form builder for reactive forms.
     * @param authService Authentication service.
     * @param webService Web service for API calls.
     */
    constructor(
        public dataService: DataService, 
        private route: ActivatedRoute,
        private router: Router,
        private formBuilder: FormBuilder, 
        public authService: AuthService, 
        private webService: WebService
    ) {}

    /**
     * Lifecycle hook that is called after data-bound properties are initialized.
     * Initializes forms and loads listing data.
     */
    ngOnInit() {
        this.initializeForms();
        this.loadListingData();
    }

    /**
     * Initializes the review and edit forms with default values and validators.
     */
    initializeForms() {
        this.reviewForm = this.formBuilder.group({
            user_name: ['', Validators.required],
            comments: ['', Validators.required],
            date: this.getCurrentDate()
        });

        this.editForm = this.formBuilder.group({
            name: ['', Validators.required],
            description: [''],
            property_type: [''],
            room_type: [''],
            accomodates: [''],
            bathrooms: [''],
            bedrooms: [''],
            beds: [''],
            amenities: [''],
            price: [''],
            minimum_nights: [''],
            maximum_nights: [''],
            review_scores_rating: ['', [Validators.required, Validators.min(0), Validators.max(5)]],
            review_scores_location: [''],
            neighbourhood: ['']
        });
    }

    /**
     * Loads listing data from the web service and sets up the map and weather information.
     */
    loadListingData() {
        this.webService.getListing(this.route.snapshot.paramMap.get('id')).subscribe((response: any) => {
            this.listing_list = [response];
            this.setupMapAndWeather();
            
            // Populate edit form with current values
            this.editForm.patchValue({
                name: this.listing_list[0].name,
                description: this.listing_list[0].description,
                property_type: this.listing_list[0].property_type,
                room_type: this.listing_list[0].room_type,
                accomodates: this.listing_list[0].accomodates,
                bathrooms: this.listing_list[0].bathrooms,
                bedrooms: this.listing_list[0].bedrooms,
                beds: this.listing_list[0].beds,
                amenities: Array.isArray(this.listing_list[0].amenities) 
                    ? this.listing_list[0].amenities.join(',') 
                    : this.listing_list[0].amenities,
                price: this.listing_list[0].price,
                minimum_nights: this.listing_list[0].minimum_nights,
                maximum_nights: this.listing_list[0].maximum_nights,
                review_scores_rating: this.listing_list[0].review_scores_rating,
                review_scores_location: this.listing_list[0].review_scores_location,
                neighbourhood: this.listing_list[0].neighbourhood
            });

            this.dataService.getLoremIpsum(1).subscribe((response: any) => {
                this.loremIpsum = response.text.slice(0, 200);
            });
        });

        this.loadReviews();
    }

    /**
     * Loads reviews for the current listing from the web service.
     */
    loadReviews() {
        this.webService.getReviews(
            this.route.snapshot.paramMap.get('id'))
            .subscribe((response) => {
                this.review_list = response;
            });
    }

    /**
     * Sets up the map and weather information based on the listing's location.
     */
    setupMapAndWeather() {
        this.listing_lat = this.listing_list[0].location.coordinates[1];
        this.listing_lng = this.listing_list[0].location.coordinates[0];

        this.map_locations = [{
            lat: this.listing_lat,
            lng: this.listing_lng
        }];

        this.map_options = {
            mapId: "DEMO_MAP_ID",
            center: { lat: this.listing_lat, lng: this.listing_lng },
            zoom: 13,
        };

        this.loadWeatherData();
    }

    /**
     * Loads current weather data for the listing's location from the data service.
     */
    loadWeatherData() {
        this.dataService.getCurrentWeather(this.listing_lat, this.listing_lng).subscribe((response: any) => {
            let weatherResponse = response['weather'][0]['description'];
            this.temperature = Math.round(response['main']['temp']);
            this.weather = weatherResponse[0].toUpperCase() + weatherResponse.slice(1);
            this.weatherIcon = response['weather'][0]['icon'];
            this.weatherIconURL = "https://openweathermap.org/img/wn/" + this.weatherIcon + "@4x.png";
            this.temperatureColour = this.dataService.getTemperatureColour(this.temperature);
        });
    }

    /**
     * Toggles the edit mode for the listing.
     * Resets the form with current values when canceling edit.
     */
    toggleEdit() {
        this.isEditing = !this.isEditing;
        if (!this.isEditing) {
            // Reset form with current values when canceling edit
            this.loadListingData();
        }
    }

    /**
     * Updates the listing with the values from the edit form.
     * @returns void
     */
    onUpdate() {
        if (this.editForm.valid) {
            const listingId = this.route.snapshot.paramMap.get('id');
            if (listingId) {  
                this.webService.updateListing(
                    listingId,
                    this.editForm.value
                ).subscribe({
                    next: () => {  
                        this.isEditing = false;
                        this.loadListingData();
                    },
                    error: (error) => {
                        console.error('Error updating listing:', error);
                    }
                });
            }
        }
    }
    
    /**
     * Deletes the current listing after user confirmation.
     * @returns void
     */
    onDelete() {
        if (confirm('Are you sure you want to delete this listing? This action cannot be undone.')) {
            const listingId = this.route.snapshot.paramMap.get('id');
            if (listingId) {  // Add null check
                this.webService.deleteListing(listingId).subscribe({
                    next: () => {
                        this.router.navigate(['/listings']);
                    },
                    error: (error) => {
                        console.error('Error deleting listing:', error);
                    }
                });
            }
        }
    }

    /**
     * Submits a new review for the listing.
     * @returns void
     */
    onSubmit() {
        if (this.reviewForm.valid) {
            this.webService.postReview(
                this.route.snapshot.paramMap.get('id'),
                this.reviewForm.value
            ).subscribe({
                next: (response) => {
                    this.reviewForm.reset();
                    this.reviewForm.patchValue({ date: this.getCurrentDate() });
                    this.refreshReviews();
                    this.refreshListing();
                },
                error: (error) => {
                    console.error('Error posting review:', error);
                }
            });
        }
    }

    /**
     * Gets the current date in YYYY-MM-DD format.
     * @returns The current date as a string.
     */
    getCurrentDate(): string {
        return new Date().toISOString().split('T')[0];
    }
    
    /**
     * Refreshes the reviews for the listing.
     * @returns void
     */
    private refreshReviews() {
        this.webService.getReviews(
            this.route.snapshot.paramMap.get('id')
        ).subscribe(response => {
            this.review_list = response;
        });
    }
    
    /**
     * Refreshes the listing data.
     * @returns void
     */
    private refreshListing() {
        this.webService.getListing(
            this.route.snapshot.paramMap.get('id')
        ).subscribe((response: any) => {
            this.listing_list = [response];
        });
    }

    /**
     * Checks if a form control is invalid and has been touched.
     * @param control The name of the form control.
     * @returns True if the control is invalid and touched, false otherwise.
     */
    isInvalid(control: string) {
        return this.reviewForm.controls[control].invalid &&
            this.reviewForm.controls[control].touched;
    }

    /**
     * Checks if the review form controls are untouched.
     * @returns True if the form controls are pristine, false otherwise.
     */
    isUntouched() {
        return this.reviewForm.controls.user_name.pristine || 
               this.reviewForm.controls.comments.pristine;
    }

    /**
     * Checks if the review form is incomplete.
     * @returns True if the form is invalid or untouched, false otherwise.
     */
    isIncomplete() {
        return this.isInvalid('user_name') || 
               this.isInvalid('comments') || 
               this.isUntouched();
    }
}