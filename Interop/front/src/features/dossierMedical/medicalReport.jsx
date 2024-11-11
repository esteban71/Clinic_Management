import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faStreetView} from "@fortawesome/free-solid-svg-icons"
import React from 'react';
import {useNavigate} from 'react-router-dom';

const MedicalReport = ({report, ReportID}) => {
    const navigate = useNavigate();

    const handleView = () => {
        navigate(`/dash/patients/${ReportID}/reports`);
    };

    return (
        <tr className="table__row">
            <td className="table__cell">{report.id}</td>
            <td className="table__cell">{report.title}</td>
            <td className="table__cell">{report.content}</td>
            <td className="table__cell">{report.date}</td>
            <td className="table__cell">
                <button
                    className="icon-button table__button"
                    onClick={handleView}
                >
                    <FontAwesomeIcon icon={faStreetView}/>
                    View
                </button>
            </td>
        </tr>
    );
};

export default MedicalReport;
