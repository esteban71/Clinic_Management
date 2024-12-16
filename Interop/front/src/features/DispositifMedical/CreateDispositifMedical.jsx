import React, {useState} from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import {
    useAddNewDispositifMedicalMutation,
    useDeleteDispositifMedicalMutation,
    useUpdateDispositifMedicalMutation
} from './DispositifMedicalApiSlice.jsx';
import {MenuItem, Select} from "@mui/material";

const CreateDispositifMedical = ({existingDevice, patient_id, onClose}) => {
        const [name, setName] = useState(existingDevice?.name || '');
        const [type, setType] = useState(existingDevice?.type || '');
        const [interval, setInterval] = useState(existingDevice?.interval || '');
        const [status, setStatus] = useState(existingDevice?.status || '');
        const [manufacturer, setManufacturer] = useState(existingDevice?.manufacturer || '');
        const [serialNumber, setSerialNumber] = useState(existingDevice?.serial_number || '');
        const [lotNumber, setLotNumber] = useState(existingDevice?.lot_number || '');
        const [manufactureDate, setManufactureDate] = useState(existingDevice?.manufacture_date ? new Date(existingDevice.manufacture_date).toISOString().split('T')[0] : '');
        const [expirationDate, setExpirationDate] = useState(existingDevice?.expiration_date ? new Date(existingDevice.expiration_date).toISOString().split('T')[0] : '');

        const [createDispositifMedical,
            {
                isLoading,
                isSuccess,
                isError,
                error
            }
        ] = useAddNewDispositifMedicalMutation();
        const [updateDispositifMedical,
            {
                isLoading: isUpdateLoading,
                isSuccess: isUpdateSuccess,
                isError: isUpdateError,
                error: updateError
            }
        ] = useUpdateDispositifMedicalMutation();

        const [deleteDispositifMedical,
            {
                isSuccess: isDelSuccess,
                isError: isDelError,
                error: delerror

            }
        ] = useDeleteDispositifMedicalMutation();

        const onDelete = async () => {
            let error = await deleteDispositifMedical({
                report_id: parseInt(existingDevice.id),
                patient_id: parseInt(patient_id)
            });
            if (error.error) {
                console.error('Failed to delete device:', error);
                alert('Error deleting device! Please try again.');
                return;
            }
            onClose();
        }


        const handleSubmit = async (e) => {
                e.preventDefault();
                const deviceData = {
                    name,
                    type,
                    interval,
                    status,
                    manufacturer,
                    serial_number: serialNumber,
                    lot_number: lotNumber,
                    manufacture_date: manufactureDate,
                    expiration_date: expirationDate,
                };

                if (existingDevice) {
                    let error = await updateDispositifMedical({
                            report_id: parseInt(existingDevice.id),
                            patient_id: parseInt(patient_id)
                            , ...deviceData
                        })
                    ;
                    if (error.error) {
                        console.error('Failed to update device:', error);
                        alert('Error updating device! Please try again.');
                        return;
                    }
                } else {
                    let error = await createDispositifMedical({patient_id: parseInt(patient_id), ...deviceData});
                    if (error.error) {
                        console.error('Failed to create device:', error);
                        alert('Error creating device! Please try again.');
                        return;

                    }
                }

                onClose();
            }
        ;

        return (
            <form onSubmit={handleSubmit}>
                <TextField label="Name" value={name} onChange={(e) => setName(e.target.value)} fullWidth
                           margin="normal"/>
                <div className="form__row">
                    <div className="form__divider">
                        <label className="form__label form__checkbox-container" htmlFor="note-username">
                            TYPE:</label>
                        <Select
                            id="note-username"
                            label="Type"
                            value={type}
                            onChange={(e) => setType(e.target.value)}
                            fullWidth
                            margin="normal"
                            className="form__select"
                        >
                            <MenuItem value="Blood Pressure Monitor">Blood Pressure Monitor</MenuItem>
                            <MenuItem value="Heart Rate Monitor">Heart Rate Monitor</MenuItem>
                            <MenuItem value="Oxygen Saturation Monitor">Oxygen Saturation Monitor</MenuItem>
                        </Select>
                    </div>
                </div>
                <TextField label="Interval" value={interval} onChange={(e) => setInterval(e.target.value)}
                           fullWidth
                           margin="normal"/>
                <div className="form__row">
                    <div className="form__divider">
                        <label className="form__label form__checkbox-container" htmlFor="note-username">
                            STATUS:</label>
                        <Select
                            id="note-username"
                            label="Status"
                            value={status}
                            onChange={(e) => setStatus(e.target.value)}
                            fullWidth
                            margin="normal"
                            className="form__select"
                        >
                            <MenuItem value="active">Active</MenuItem>
                            <MenuItem value="inactive">Inactive</MenuItem>
                        </Select>
                    </div>
                </div>

                <TextField label="Manufacturer" value={manufacturer}
                           onChange={(e) => setManufacturer(e.target.value)}
                           fullWidth margin="normal"/>
                <TextField label="Serial Number" value={serialNumber}
                           onChange={(e) => setSerialNumber(e.target.value)}
                           fullWidth margin="normal"/>
                <TextField label="Lot Number" value={lotNumber} onChange={(e) => setLotNumber(e.target.value)}
                           fullWidth
                           margin="normal"/>
                <TextField label="Manufacture Date" type="date" value={manufactureDate}
                           onChange={(e) => setManufactureDate(e.target.value)} fullWidth margin="normal"
                           InputLabelProps={{shrink: true}}/>
                <TextField label="Expiration Date" type="date" value={expirationDate}
                           onChange={(e) => setExpirationDate(e.target.value)} fullWidth margin="normal"
                           InputLabelProps={{shrink: true}}/>
                <Button type="submit" variant="contained" color="primary">Save</Button>
                <Button onClick={onDelete} variant="contained" color="secondary">Delete</Button>
                <Button onClick={onClose} variant="contained" sx={{backgroundColor: 'gray', color: 'white'}}>Cancel</Button>
            </form>
        );
    }
;

export default CreateDispositifMedical;