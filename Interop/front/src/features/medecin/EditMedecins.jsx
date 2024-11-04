import React from 'react'
import {useParams} from 'react-router-dom'
import {useSelector} from 'react-redux'
import {selectMedecinById} from "./medecinApiSlice.jsx";
import EditMedecinsForm from "./EditMedecinsForm.jsx";
import CircularLoader from '../../pageLoader/CircularLoader.jsx'

const EditMedecins = () => {

    const {id} = useParams()

    const doctor = useSelector(state => selectMedecinById(state, id))

    const content = doctor ? <EditMedecinsForm doctor={doctor}/> : <CircularLoader/>

    return content

}

export default EditMedecins
