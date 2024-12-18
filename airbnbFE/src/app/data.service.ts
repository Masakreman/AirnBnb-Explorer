import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

/**
 * A service for fetching various data from external APIs.
 * Currently supports getting Lorem Ipsum text and weather data.
 */
@Injectable({
    providedIn: 'root'
})
export class DataService {
    /**
     * Sets up our service with HTTP capabilities
     */
    constructor(private http: HttpClient) { }

    /**
     * Grabs some Lorem Ipsum text from API Ninjas
     * @param paragraphs - How many paragraphs you want
     * @returns Observable with the Lorem Ipsum text
     */
    getLoremIpsum(paragraphs: number): Observable<any> {
        let API_key = 'se8iMQVK7YvPwVR2v7pAgQ==XuyjlTXln7YxU6eT';
        return this.http.get<any>(
            'https://api.api-ninjas.com/v1/loremipsum?paragraphs=' + paragraphs,
            { headers: { 'X-Api-Key': API_key } }
        );
    }

    /**
     * Fetches current weather data based on coordinates
     * @param lat - Latitude of the location
     * @param lon - Longitude of the location
     * @returns Observable with weather details from OpenWeatherMap
     */
    getCurrentWeather(lat: number, lon: number) {
        let API_key = "5358fa926cd6340d99ca4b81f9a6ecc9";
        return this.http.get<any>(
            'https://api.openweathermap.org/data/2.5/weather?lat=' + lat +
            '&lon=' + lon + '&units=metric&appid=' + API_key
        );
    }

    /**
     * Picks a color to represent a temperature
     * @param temp - Temperature in Celsius
     * @returns A hex color code:
     * - Blue for freezing (≤5°C)
     * - Green for cool (≤12°C)
     * - Yellow for mild (≤17°C)
     * - Orange for warm (≤25°C)
     * - Red for hot (>25°C)
     */
    getTemperatureColour(temp: number) {
        if (temp <= 5) return "#0000ff";
        else if (temp <= 12) return "#00ff00";
        else if (temp <= 17) return "#ffff00";
        else if (temp <= 25) return "#ff7f00";
        else return "#ff0000"
    }
}