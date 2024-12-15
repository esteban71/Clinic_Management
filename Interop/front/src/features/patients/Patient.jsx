import React from 'react'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faStreetView} from "@fortawesome/free-solid-svg-icons"
import {useNavigate} from 'react-router-dom'
import {useSelector} from 'react-redux'
import {selectPatientById} from './patientsApiSlice.jsx'
import useAuth from "../../hooks/useAuth.jsx";


const Patient = ({patientID}) => {

    const {username, isManager, isAdmin, isDoctor, isReceptionist} = useAuth()

    const patient = useSelector(state => selectPatientById(state, patientID))

    const navigate = useNavigate()

    if (patient) {

        const handleEdit = () => navigate(`/dash/patients/${patientID}`)

        //const deceaseRecordOne = patient.deceaseRecordOne
        //const medicineRecordOne = patient.medicineRecordOne
        //const deceaseRecordTwo = patient.deceaseRecordTwo
        //const medicineRecordTwo = patient.medicineRecordTwo
        // const doctorID = patient.medecin.id

        const handleViewAllReport = () => {
            navigate(`/dash/patients/${patientID}/reports`)
        }

        const handleViewAllDispositifs = () => {
            navigate(`/dash/patients/${patientID}/dispositifs`)
        }

        return (
            <tr className="table__row">
                <td className="table__cell">{patient.id}</td>
                <td className="table__cell">{patient.name}</td>
                <td className="table__cell">{patient.address}</td>
                <td className="table__cell">{patient.telecom}</td>
                <td className="table__cell">
                    <button
                        className="icon-button table__button"
                        onClick={handleEdit}
                    >
                        <FontAwesomeIcon icon={faStreetView}/>
                    </button>
                </td>
                {(isManager || isAdmin || isDoctor) ? (
                    <td className="table__cell">
                        <button
                            className="icon-button table__button"
                            onClick={handleViewAllReport}
                        >
                            <FontAwesomeIcon icon={faStreetView}/>
                        </button>
                    </td>
                ) : (
                    <td className="table__cell">No Access</td>
                )}
                {(isManager || isAdmin || isDoctor) ? (
                    <td className="table__cell">
                        <button
                            className="icon-button table__button"
                            onClick={handleViewAllDispositifs}
                        >
                            <FontAwesomeIcon icon={faStreetView}/>
                        </button>
                    </td>
                ) : (
                    <td className="table__cell">No Access</td>
                )}

            </tr>
        )
    } else return null
}

export default Patient
