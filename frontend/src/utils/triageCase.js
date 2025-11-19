import {
  UrgencyCellRenderer,
  urgencyComparator,
  dateTimeFormatter,
  ageValueGetter,
  EditButtonCellRenderer,
} from './gridUtils';

export const triageCaseColumnDefs = [
  {
    headerName: 'Urgency',
    field: 'urgencyLevel',
    flex: 0.75,
    cellRenderer: UrgencyCellRenderer,
    filter: 'agTextColumnFilter',
    comparator: urgencyComparator,
    sort: "asc"
  },
  {
    headerName: 'Patient Name',
    field: 'name',
    flex: 0.75,
    filter: 'agTextColumnFilter',
  },
  {
    headerName: 'Age',
    field: 'dob',
    flex: 0.5,
    filter: 'agNumberColumnFilter',
    valueGetter: (params) => ageValueGetter(params.data?.dob),
  },
  {
    headerName: 'Date',
    field: 'dateCreated',
    flex: 0.75,
    valueFormatter: dateTimeFormatter,
    filter: 'agDateColumnFilter',
    sort: 'desc',
  },
  {
    headerName: 'AI Summary',
    field: 'aiSummary',
    flex: 6,
    tooltipField: 'aiSummary',
    filter: 'agTextColumnFilter',
  },
  {
    headerName: 'Edit',
    flex: 0.5,
    cellRenderer: EditButtonCellRenderer
  },
];