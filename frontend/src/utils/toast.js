import { toast } from 'react-toastify';

const defaultOptions = {
  position: "bottom-right",
  autoClose: 3000,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
};

export const showToast = (message, type = 'success') => {
  toast[type](message, defaultOptions);
};