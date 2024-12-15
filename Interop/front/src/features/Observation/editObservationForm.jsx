import React, {useEffect, useState} from 'react';
import {useDeleteObservationMutation} from './ObservationApiSlice.jsx';
import {useNavigate} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faTrashCan} from '@fortawesome/free-solid-svg-icons';
import TextField from '@mui/material/TextField';
import '../../css/observation.css';

const EditObservationForm = ({report, patientID}) => {
    const formatDateTime = (dateTime) => {
        const date = new Date(dateTime);
        return date.toISOString().slice(0, 16);
    };

    const [date_time, setDateTime] = useState(formatDateTime(report.date_time));
    const [code, setCode] = useState(report.code);
    const [value, setValue] = useState(report.value);
    const [unit, setUnit] = useState(report.unit);
    const [status, setStatus] = useState(report.status);
    const [component_code, setComponentCode] = useState(report.component_code);
    const [component_value, setComponentValue] = useState(report.component_value);
    const [component_unit, setComponentUnit] = useState(report.component_unit);

    const [deleteObservation, {
        isSuccess: isDelSuccess,
        isError: isDelError,
        error: delerror
    }] = useDeleteObservationMutation();
    const navigate = useNavigate();

    useEffect(() => {
        if (isDelSuccess) {
            setDateTime('');
            setCode('');
            setValue('');
            setUnit('');
            setStatus('');
            setComponentCode('');
            setComponentValue('');
            setComponentUnit('');
            navigate(`/dash/patients/${patientID}/dispositifs`);
        }
    }, [isDelSuccess, navigate, patientID]);

    const onDeleteReportClicked = async () => {
        const result = await deleteObservation({report_id: parseInt(report.id), patient_id: parseInt(patientID)});
        if (result.error) {
            console.error('Failed to delete observation:', result.error);
            alert('Error deleting observation! Please try again.');
        } else {
            alert('Observation deleted successfully!');
        }
    };

    const errClass = isDelError ? "errmsg" : "offscreen";
    const errContent = delerror?.data?.message ?? '';

    return (
        <>
            <p className={errClass}>{errContent}</p>
            <form className="form" onSubmit={(e) => e.preventDefault()}>
                <div className="form__title-row">
                    <h2>Observation Details [ID: {report.id}]</h2>
                    <div className="form__action-buttons">
                        <button
                            className="icon-button"
                            title="Delete"
                            onClick={onDeleteReportClicked}
                        >
                            <FontAwesomeIcon icon={faTrashCan}/>
                        </button>
                    </div>
                </div>

                <div className="observation-form">
                    <TextField
                        label="Date Time"
                        name="date_time"
                        type="datetime-local"
                        variant="outlined"
                        value={date_time}
                        fullWidth
                        margin="normal"
                        InputLabelProps={{
                            shrink: true,
                        }}
                        disabled
                    />

                    <TextField
                        label="Code"
                        name="code"
                        variant="outlined"
                        value={code}
                        fullWidth
                        margin="normal"
                        disabled
                    />

                    <TextField
                        label="Value"
                        name="value"
                        variant="outlined"
                        value={value}
                        fullWidth
                        margin="normal"
                        disabled
                    />

                    <TextField
                        label="Unit"
                        name="unit"
                        variant="outlined"
                        value={unit}
                        fullWidth
                        margin="normal"
                        disabled
                    />

                    <TextField
                        label="Status"
                        name="status"
                        variant="outlined"
                        value={status}
                        fullWidth
                        margin="normal"
                        disabled
                    />

                    <TextField
                        label="Component Code"
                        name="component_code"
                        variant="outlined"
                        value={component_code}
                        fullWidth
                        margin="normal"
                        disabled
                    />

                    <TextField
                        label="Component Value"
                        name="component_value"
                        variant="outlined"
                        value={component_value}
                        fullWidth
                        margin="normal"
                        disabled
                    />

                    <TextField
                        label="Component Unit"
                        name="component_unit"
                        variant="outlined"
                        value={component_unit}
                        fullWidth
                        margin="normal"
                        disabled
                    />
                </div>
            </form>
        </>
    );
};

export default EditObservationForm;