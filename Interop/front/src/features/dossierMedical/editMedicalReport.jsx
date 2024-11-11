import React, {useSelector} from 'react';
import {useParams} from 'react-router-dom';
import EditMedicalReportForm from './editMedicalReportForm';
import {selectMedicalReportById} from './medicalReportsApiSlice.jsx';

const EditMedicalReport = () => {
    const {id, patientID} = useParams();
    const report = useSelector(state => selectMedicalReportById(state, id));

    const content = report && medecin ? <EditMedicalReportForm report={report} patientID={patientID}/> :
        <p>Loading...</p>;

    console.log('content', content);

    return content;
};

export default EditMedicalReport;
