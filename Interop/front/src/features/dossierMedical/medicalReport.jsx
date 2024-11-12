import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faStreetView} from "@fortawesome/free-solid-svg-icons"
import React from 'react';
import {useNavigate} from 'react-router-dom';

const MedicalReport = ({report}) => {
    const navigate = useNavigate();
    const PatientID = window.location.href.split('/')[5];
    const reportID = report.id;
    const handleView = () => {
        navigate(`/dash/patients/${PatientID}/reports/${reportID}`);
    };

    return (
        <tr className="table__row">
            <td className="table__cell">{report.id}</td>
            <td className="table__cell">{report.date}</td>
            <td className="table__cell">{report.title}</td>
            <td className="table__cell">{report.content}</td>
            <td className="table__cell">
                <button
                    className="icon-button table__button"
                    onClick={handleView}
                >
                    <FontAwesomeIcon icon={faStreetView}/>
                    Edit
                </button>
            </td>
            <td className="table__cell">{report.auteur}</td>
        </tr>
    );
};

export default MedicalReport;
