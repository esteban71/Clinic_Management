import React, { useEffect, useState } from 'react';
import { useDeleteMedicalReportMutation, useUpdateMedicalReportMutation } from './medicalReportsApiSlice.jsx';
import { useNavigate, useParams } from 'react-router-dom'; // Importer useParams
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSave, faTrashCan } from '@fortawesome/free-solid-svg-icons';
import TextField from '@mui/material/TextField';

const EditMedicalReportForm = ({ report }) => {
    const { patientID } = useParams();
    const [updateMedicalReport, { isLoading, isSuccess, isError, error }] = useUpdateMedicalReportMutation();

    console.log('report:', report);

    // Initialisation des états pour les champs du formulaire
    const [title, setTitle] = useState(report.title);
    const [content, setContent] = useState(report.content);
    const [date, setDate] = useState(report.date);

    const [deleteMedicalReport, {
        isSuccess: isDelSuccess,
        isError: isDelError,
        error: delerror
    }] = useDeleteMedicalReportMutation()
    const navigate = useNavigate();

    useEffect(() => {
        if (isSuccess) {
            // Réinitialiser les champs après une mise à jour réussie
            setTitle('');
            setContent('');
            setDate('');
            navigate(`/dash/patients/${patientID}/reports/${report.id}`);
        }
    }, [isSuccess, navigate, patientID]);

    const onTitleChanged = (e) => setTitle(e.target.value);
    const onContentChanged = (e) => setContent(e.target.value);
    const onDateChanged = (e) => setDate(e.target.value);

    const canSave = [title, content, date].every(Boolean) && !isLoading;

    const onSaveReportClicked = async (e) => {
        e.preventDefault();
        if (canSave) {
            try {
                await updateMedicalReport({
                    id: report.id,
                    patient_id: patientID,
                    title,
                    content,
                    date
                }).unwrap();
                alert('Medical report updated successfully!');
            } catch (err) {
                console.error('Failed to update medical report:', err);
                alert('Error updating report! Please try again.');
            }
        } else {
            alert('Please fill out all fields.');
        }
    };

    const onDeleteReportClicked = async (e) => {
        await deleteMedicalReport(report.id);
        alert('Medical report deleted successfully!');
    };

    const errClass = isError ? "errmsg" : "offscreen";
    const errContent = error?.data?.message ?? '';

    const contentForm = (
        <>
            <p className={errClass}>{errContent}</p>
            <form className="form" onSubmit={(e) => e.preventDefault()}>
                <div className="form__title-row">
                    <h2>Edit Medical Report [ID: {report.id}]</h2>
                    <div className="form__action-buttons">
                        <button
                            className="icon-button"
                            title="Save"
                            onClick={onSaveReportClicked}
                            disabled={!canSave}
                        >
                            <FontAwesomeIcon icon={faSave} />
                        </button>
                        <button
                                className="icon-button"
                                title="Delete"
                                onClick={onDeleteReportClicked}
                            >
                                <FontAwesomeIcon icon={faTrashCan}/>
                            </button>
                    </div>
                </div>

                <div className="medical-report-form">
                    <TextField
                        label="Report Title"
                        name="title"
                        variant="outlined"
                        value={title}
                        onChange={onTitleChanged}
                        fullWidth
                        required
                        margin="normal"
                    />

                    <TextField
                        label="Report Content"
                        name="content"
                        variant="outlined"
                        value={content}
                        onChange={onContentChanged}
                        fullWidth
                        required
                        multiline
                        rows={4}
                        margin="normal"
                    />

                    <TextField
                        label="Report Date"
                        name="date"
                        type="date"
                        variant="outlined"
                        value={date}
                        onChange={onDateChanged}
                        fullWidth
                        required
                        margin="normal"
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />
                </div>
            </form>
        </>
    );

    return contentForm;
};

export default EditMedicalReportForm;
