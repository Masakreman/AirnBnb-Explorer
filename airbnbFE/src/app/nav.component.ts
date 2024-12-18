import { Component } from '@angular/core';
import { RouterOutlet, RouterModule } from '@angular/router';
import { AuthButtonComponent } from './authbutton.component';
import { AuthUserComponent } from './authuser.component';

/**
 * Navigation component that serves as the main navigation container for the application.
 * Integrates routing functionality and authentication-related components.
 * 
 * @class NavComponent
 * @implements {Component}
 * 
 * @description
 * This navbar component has:
 * - Angular Router functionality for navigation
 * - Authentication button for login/logout actions
 * - User authentication status display
 * 
 * @example
 * <!-- Usage in template -->
 * <navigation></navigation>
 * 
 * @see {@link AuthButtonComponent}
 * @see {@link AuthUserComponent}
 */
@Component({
  selector: 'navigation',
  standalone: true,
  imports: [RouterOutlet, RouterModule, AuthButtonComponent, AuthUserComponent],
  templateUrl: './nav.component.html',
})
export class NavComponent {
  
}
