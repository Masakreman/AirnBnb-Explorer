/**
 * @file authuser.component.ts
 * @description This file defines the `AuthUserComponent`, which handles user profile information 
 *              and interacts with Auth0 for authentication and user management. It leverages Angular's 
 *              `AsyncPipe` for binding asynchronous data streams directly in the template.
 */

import { Component } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { AsyncPipe } from '@angular/common';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'user-profile',
    templateUrl: 'authuser.component.html',
    standalone: true,
    imports: [AsyncPipe, CommonModule]
})
export class AuthUserComponent {
    /**
     * @constructor
     * @param {AuthService} auth - The Auth0 authentication service used to manage authentication 
     *                              and user profile information.
     */
    constructor(public auth: AuthService) {}
}
