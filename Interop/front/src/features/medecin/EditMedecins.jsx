import React from 'react'
import {useParams} from 'react-router-dom'
import {useSelector} from 'react-redux'
import {selectMedecinById} from "./medecinApiSlice.jsx";
import EditMedecinsForm from "./EditMedecinsForm.jsx";
import CircularLoader from '../../pageLoader/CircularLoader.jsx'
import {selectAllCabinets} from "../cabinet/cabinetApiSlice.jsx";

const EditMedecins = () => {

    const {id} = useParams()

    const doctor = useSelector(state => selectMedecinById(state, id))
    const cabinet_data = useSelector(selectAllCabinets)
    const cabinet = doctor ? cabinet_data.length ? cabinet_data.find(cabinet => cabinet.id === doctor.cabinet_medical_id) : null : null

    const content = doctor ? <EditMedecinsForm doctor={doctor} allcabinet={cabinet_data} cabinet={cabinet}/> :
        <CircularLoader/>

    return content

}

export default EditMedecins
