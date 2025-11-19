import {
  UrgencyCellRenderer,
  urgencyComparator,
  dateTimeFormatter,
} from '../utils/gridUtils';

export const triageCaseColumnDefs = [
  {
    headerName: 'Urgency Level',
    field: 'urgencyLevel',
    width: 150,
    cellRenderer: UrgencyCellRenderer,
    filter: 'agTextColumnFilter',
    comparator: urgencyComparator,
    sort: "asc"
  },
  {
    headerName: 'Patient Name',
    field: 'name',
    width: 180,
    filter: 'agTextColumnFilter',
  },
  {
    headerName: 'Age',
    width: 100,
    filter: 'agNumberColumnFilter',
  },
  {
    headerName: 'Date',
    field: 'dateCreated',
    width: 150,
    valueFormatter: dateTimeFormatter,
    filter: 'agDateColumnFilter',
    sort: 'desc',
  },
  {
    headerName: 'AI Summary',
    field: 'aiSummary',
    flex: 1,
    minWidth: 300,
    tooltipField: 'aiSummary',
    filter: 'agTextColumnFilter',
    wrapText: false,
  },
];