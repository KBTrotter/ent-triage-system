import {
  Box,
  Dialog,
  DialogContent,
  DialogActions,
  DialogTitle,
  Button,
  TextField,
  Typography,
} from "@mui/material";
import { useFormik } from "formik";
import * as Yup from "yup";
export default function ResolveCaseDialog({
  open,
  onClose,
  onResolve,
  initialResolvedBy,
}) {
  const formik = useFormik({
    enableReinitialize: true,
    initialValues: {
      resolutionReason: "",
      resolvedBy: initialResolvedBy || "",
    },
    validationSchema: Yup.object({
      resolutionReason: Yup.string().required("Resolution reason is required"),
    }),
    onSubmit: (values) => {
      onResolve({
        resolutionReason: values.resolutionReason,
        resolvedBy: values.resolvedBy,
      });
      formik.resetForm();
      console.log("Resolution Details: ", values);
    },
  });

  const handleClose = () => {
    formik.resetForm();
    onClose();
  };
  
  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Please Enter Resolution Details:</DialogTitle>
      <DialogContent>
        <form onSubmit={formik.handleSubmit}>
          <TextField
            fullWidth
            multiline
            margin="normal"
            name="resolutionReason"
            label="Resolution Reason"
            value={formik.values.resolutionReason}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={Boolean(formik.errors.resolutionReason)}
            helperText={
              formik.touched.resolutionReason && formik.errors.resolutionReason
            }
          />
          <Box>
            <Typography variant="subtitle1" color="textSecondary">
              Resolved By:
            </Typography>
            <Typography variant="body1" margin="normal">
              {formik.values.resolvedBy}
            </Typography>
          </Box>
        </form>
      </DialogContent>
      <DialogActions>
        <Button onClick={formik.handleSubmit} variant="contained">
          Resolve
        </Button>
        <Button onClick={handleClose}>Cancel</Button>
      </DialogActions>
    </Dialog>
  );
}
