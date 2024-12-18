import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { WebService } from './web.service';

describe('WebService', () => {
  let service: WebService;
  let httpMock: HttpTestingController;
  const baseUrl = 'http://127.0.0.1:5000/api/v1.0';

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [WebService]
    });

    service = TestBed.inject(WebService);
    httpMock = TestBed.inject(HttpTestingController);

    // Handle the initial getAllListings call from constructor
    const req = httpMock.expectOne(`${baseUrl}/listings?pn=1&ps=3000`);
    req.flush([{ id: 1 }, { id: 2 }]); // Mock response for initial call
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should handle paginated listings request', () => {
    const mockListings = [
      { id: 1, name: 'Test 1' },
      { id: 2, name: 'Test 2' }
    ];

    service.getListings(1).subscribe(listings => {
      expect(listings).toEqual(mockListings);
    });

    const req = httpMock.expectOne(`${baseUrl}/listings?pn=1&ps=6`);
    expect(req.request.method).toBe('GET');
    req.flush(mockListings);
  });

  it('should handle single listing request', () => {
    const mockListing = { id: '123', name: 'Test Listing' };

    service.getListing('123').subscribe(listing => {
      expect(listing).toEqual(mockListing);
    });

    const req = httpMock.expectOne(`${baseUrl}/listings/123`);
    expect(req.request.method).toBe('GET');
    req.flush(mockListing);
  });

  it('should calculate correct last page number', () => {
    // Since we mocked 2 listings in the constructor response
    // and pageSize is 6, we should get 1 as the last page
    expect(service.getLastPageNumber()).toBe(1);
  });
});