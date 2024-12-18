import { ComponentFixture, TestBed } from '@angular/core/testing';
import { GridComponent } from './grid.component';
import { WebService } from './web.service';
import { AgGridAngular } from 'ag-grid-angular';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('GridComponent', () => {
  let component: GridComponent;
  let fixture: ComponentFixture<GridComponent>;
  let mockWebService: jasmine.SpyObj<WebService>;

  beforeEach(async () => {
    mockWebService = jasmine.createSpyObj('WebService', ['getAllListings']);

    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        AgGridAngular,
        GridComponent
      ],
      providers: [
        { provide: WebService, useValue: mockWebService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(GridComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize with correct column definitions', () => {
    expect(component.headings.length).toBe(6);
    expect(component.headings[0].field).toBe('name');
  });

  it('should have correct pagination settings', () => {
    expect(component.pagination).toBeTrue();
    expect(component.paginationPageSize).toBe(10);
    expect(component.paginationPageSizeSelector).toEqual([10, 25, 50, 100]);
  });
});