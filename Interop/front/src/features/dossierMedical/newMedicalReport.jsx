import React from 'react';
import {useParams} from 'react-router-dom';
import NewMedicalReportForm from './newMedicalReportForm';

const NewMedicalReport = () => {
    const {patientID} = useParams();
    return <NewMedicalReportForm patientID={patientID}/>;
};

export default NewMedicalReport;
