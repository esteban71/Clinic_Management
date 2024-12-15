import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faStreetView} from "@fortawesome/free-solid-svg-icons"
import React from 'react';
import {useNavigate} from 'react-router-dom';

const ObservationReport = ({report}) => {
    const navigate = useNavigate();
    const PatientID = window.location.href.split('/')[5];
    const reportID = report.id;
    const handleView = () => {
        navigate(`/dash/patients/${PatientID}/dispositifs/${reportID}`);
    };

    return (
        <tr className="table__row">
            <td className="table__cell">{report.id}</td>
            <td className="table__cell">{report.date_time}</td>
            <td className="table__cell">{report.code}</td>
            <td className="table__cell">{report.value}</td>
            <td className="table__cell">{report.unit}</td>
            <td className="table__cell">{report.status}</td>
            <td className="table__cell">{report.component_code}</td>
            <td className="table__cell">{report.component_value}</td>
            <td className="table__cell">{report.component_unit}</td>
            <td className="table__cell">
                <button
                    className="icon-button table__button"
                    onClick={handleView}
                >
                    <FontAwesomeIcon icon={faStreetView}/>
                    Edit
                </button>
            </td>
        </tr>
    );
};

export default ObservationReport;
