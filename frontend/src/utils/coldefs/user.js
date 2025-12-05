import {
  EditUserButtonCellRenderer,
} from '../gridUtils';

export const userColumnDefs = [
  {
    headerName: 'First Name',
    field: 'firstName',
    flex: 0.5,
    minWidth: 100,
    filter: 'agTextColumnFilter',
  },
  {
    headerName: 'Last Name',
    field: 'lastName',
    flex: 0.5,
    minWidth: 100,
    filter: 'agTextColumnFilter',
  },
  {
    headerName: 'Email',
    field: 'email',
    flex: 0.5,
    minWidth: 100,
    filter: 'agTextColumnFilter',
  },
  {
    headerName: 'Role',
    field: 'role',
    flex: 0.5,
    minWidth: 150,
    filter: 'agTextColumnFilter',
  },
  {
    headerName: 'Edit',
    flex: 0.25,
    minWidth: 100,
    cellRenderer: EditUserButtonCellRenderer,
    sortable: false,
  },
];