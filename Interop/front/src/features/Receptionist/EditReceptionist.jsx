import React from 'react'
import {useParams} from 'react-router-dom'
import {useSelector} from 'react-redux'
import {selectReceptionistById} from "./ReceptionistApiSlice.jsx";
import EditReceptionistForm from "./EditReceptionistForm.jsx";
import CircularLoader from '../../pageLoader/CircularLoader.jsx'
import {selectAllCabinets} from "../cabinet/cabinetApiSlice.jsx";

const EditReceptionist = () => {

    const {id} = useParams()

    const receptionist = useSelector(state => selectReceptionistById(state, id))
    const cabinet_data = useSelector(selectAllCabinets)
    const cabinet = receptionist ? cabinet_data.length ? cabinet_data.find(cabinet => cabinet.id === receptionist.cabinet_medical_id) : null : null

    const content = receptionist ?
        <EditReceptionistForm receptionist={receptionist} allcabinet={cabinet_data} cabinet={cabinet}/> :
        <CircularLoader/>

    return content

}

export default EditReceptionist
