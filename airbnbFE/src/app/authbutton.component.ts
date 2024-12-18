import { Component, Inject } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { DOCUMENT } from '@angular/common';
import { AsyncPipe } from '@angular/common';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

/**
 * Authentication button component that handles Auth0 login/logout functionality.
 * Works in conjunction with Auth0's authentication service to manage user sessions.
 * 
 * @class AuthButtonComponent
 * @implements {Component}
 * 
 * @description
 * A standalone component that:
 * - Provides login/logout button functionality
 * - Integrates with Auth0's authentication service
 * - Handles document-level operations for auth redirects
 * - Manages routing after authentication events
 * 
 * @example
 * <!-- Usage in template -->
 * <auth-button></auth-button>
 */
@Component({
    selector: 'auth-button',
    templateUrl: 'authbutton.component.html',
    standalone: true,
    imports: [CommonModule, AsyncPipe],
    providers: [Router]
})
export class AuthButtonComponent {
    /**
     * Creates an instance of AuthButtonComponent.
     * 
     * @constructor
     * @param {Document} document - Injected Document object for DOM manipulation
     * @param {AuthService} auth - Auth0's authentication service
     * @param {Router} router - Angular router for navigation after auth events
     */
    constructor(
        @Inject(DOCUMENT) public document: Document, 
        public auth: AuthService, 
        public router: Router
    ) {}
}

