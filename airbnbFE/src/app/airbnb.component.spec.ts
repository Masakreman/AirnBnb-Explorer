import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ListingsComponent } from './airbnb.component';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { DataService } from './data.service';
import { WebService } from './web.service';
import { of } from 'rxjs';

describe('ListingsComponent', () => {
  let component: ListingsComponent;
  let fixture: ComponentFixture<ListingsComponent>;
  let webService: jasmine.SpyObj<WebService>;

  const mockListings = [
    { id: 1, name: 'Listing 1' },
    { id: 2, name: 'Listing 2' }
  ];

  beforeEach(async () => {
    const webServiceSpy = jasmine.createSpyObj('WebService', [
      'getListings',
      'getAllListings',
      'getListing',
      'postReview',
      'getReviews',
      'updateListing',
      'deleteListing',
      'getLastPageNumber'
    ]);

    webServiceSpy.getListings.and.returnValue(of(mockListings));
    webServiceSpy.getAllListings.and.returnValue(of(mockListings));
    webServiceSpy.getLastPageNumber.and.returnValue(3);
    
    Object.defineProperty(webServiceSpy, 'pageSize', {
      get: () => 6
    });

    await TestBed.configureTestingModule({
      imports: [
        ListingsComponent,
        RouterTestingModule,
        HttpClientTestingModule
      ],
      providers: [
        DataService,
        { provide: WebService, useValue: webServiceSpy }
      ]
    }).compileComponents();

    webService = TestBed.inject(WebService) as jasmine.SpyObj<WebService>;
    fixture = TestBed.createComponent(ListingsComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should not go to previous page when on page 1', fakeAsync(() => {
    component.page = 1;
    const initialCallCount = webService.getListings.calls.count();
    
    component.previousPage();
    tick();

    expect(component.page).toBe(1);
    expect(webService.getListings.calls.count()).toBe(initialCallCount);
  }));

  it('should not go to next page when on last page', fakeAsync(() => {
    component.page = 3;
    const initialCallCount = webService.getListings.calls.count();
    
    component.nextPage();
    tick();

    expect(component.page).toBe(3);
    expect(webService.getListings.calls.count()).toBe(initialCallCount);
  }));

  afterEach(() => {
    sessionStorage.clear();
  });
});