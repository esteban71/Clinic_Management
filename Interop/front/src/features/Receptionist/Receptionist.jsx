import React from 'react'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faStreetView} from "@fortawesome/free-solid-svg-icons"
import {useNavigate} from 'react-router-dom'
import {useSelector} from 'react-redux'
import {selectReceptionistById} from './ReceptionistApiSlice.jsx'


const Receptionist = ({ReceptionistID}) => {

    const Receptionist = useSelector(state => selectReceptionistById(state, ReceptionistID))

    const navigate = useNavigate()

    if (Receptionist) {

        const handleEdit = () => navigate(`/dash/receptionists/${ReceptionistID}`)

        //const deceaseRecordOne = patient.deceaseRecordOne
        //const medicineRecordOne = patient.medicineRecordOne
        //const deceaseRecordTwo = patient.deceaseRecordTwo
        //const medicineRecordTwo = patient.medicineRecordTwo
        // const doctorID = patient.Receptionist.id

        return (
            <tr className="table__row">
                <td className="table__cell">{Receptionist.id}</td>
                <td className="table__cell">{Receptionist.name}</td>
                <td className="table__cell">{Receptionist.cabinet_medical.name}</td>
                <td className="table__cell">
                    <button
                        className="icon-button table__button"
                        onClick={handleEdit}
                    >
                        <FontAwesomeIcon icon={faStreetView}/>
                    </button>
                </td>
            </tr>
        )
    } else return null
}

export default Receptionist