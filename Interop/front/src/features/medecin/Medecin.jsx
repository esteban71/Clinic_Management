import React from 'react'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faPenToSquare, faStreetView} from "@fortawesome/free-solid-svg-icons"
import {useNavigate} from 'react-router-dom'
import {useSelector} from 'react-redux'
import {selectMedecinById} from './medecinApiSlice.jsx'


const Medecin = ({medecinID}) => {

    const medecin = useSelector(state => selectMedecinById(state, medecinID))

    const navigate = useNavigate()

    if (medecin) {

        const handleEdit = () => navigate(`/dash/medecins/${medecinID}`)

        //const deceaseRecordOne = patient.deceaseRecordOne
        //const medicineRecordOne = patient.medicineRecordOne
        //const deceaseRecordTwo = patient.deceaseRecordTwo
        //const medicineRecordTwo = patient.medicineRecordTwo
        // const doctorID = patient.medecin.id

        return (
            <tr className="table__row">
                <td className="table__cell">{medecin.id}</td>
                <td className="table__cell">{medecin.name}</td>
                <td className="table__cell">{medecin.specialite}</td>
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

export default Medecin