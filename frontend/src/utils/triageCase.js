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
    flex: 0.75, // flex determines the proportion the column will take up
    minWidth: 100, // set minimum width to create overflow on smaller window sizes
    cellRenderer: UrgencyCellRenderer,
    filter: 'agTextColumnFilter',
    comparator: urgencyComparator,
    sort: "asc"
  },
  {
    headerName: 'Patient Name',
    field: 'name',
    flex: 0.75,
    minWidth: 150,
    filter: 'agTextColumnFilter',
  },
  {
    headerName: 'Age',
    field: 'dob',
    flex: 0.5,
    minWidth: 100,
    filter: 'agNumberColumnFilter',
    valueGetter: (params) => ageValueGetter(params.data?.dob),
  },
  {
    headerName: 'Date',
    field: 'dateCreated',
    flex: 0.75,
    minWidth: 200,
    valueFormatter: dateTimeFormatter,
    filter: 'agDateColumnFilter',
    sort: 'desc',
  },
  {
    headerName: 'AI Summary',
    field: 'aiSummary',
    flex: 6,
    minWidth: 300,
    tooltipField: 'aiSummary',
    filter: 'agTextColumnFilter',
  },
  {
    headerName: 'Edit',
    flex: 0.5,
    minWidth: 100,
    cellRenderer: EditButtonCellRenderer
  },
];