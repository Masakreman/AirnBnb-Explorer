import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ListingComponent } from './listing.component';
import { RouterTestingModule } from '@angular/router/testing';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { WebService } from './web.service';
import { DataService } from './data.service';
import { AuthService } from '@auth0/auth0-angular';
import { CommonModule } from '@angular/common';
import { GoogleMapsModule } from '@angular/google-maps';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('ListingComponent', () => {
  let component: ListingComponent;
  let fixture: ComponentFixture<ListingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        ReactiveFormsModule,
        CommonModule,
        GoogleMapsModule,
        HttpClientTestingModule,
        ListingComponent
      ],
      providers: [
        FormBuilder,
        { provide: WebService, useValue: jasmine.createSpyObj('WebService', ['getListing', 'getReviews']) },
        { provide: DataService, useValue: jasmine.createSpyObj('DataService', ['getLoremIpsum', 'getCurrentWeather']) },
        { provide: AuthService, useValue: {} },
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: {
                get: () => '123'
              }
            }
          }
        }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ListingComponent);
    component = fixture.componentInstance;
    component.ngOnInit();
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should mark review form as invalid when empty', () => {
    expect(component.reviewForm.valid).toBeFalse();
  });

  it('should mark review form as valid when properly filled', () => {
    component.reviewForm.controls['user_name'].setValue('Test User');
    component.reviewForm.controls['comments'].setValue('Test Comment');
    
    expect(component.reviewForm.valid).toBeTrue();
  });
});