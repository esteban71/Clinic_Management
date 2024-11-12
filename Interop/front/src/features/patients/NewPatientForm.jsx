import React, {useEffect, useState} from 'react'
import {useNavigate} from "react-router-dom"
import {useAddNewPatientMutation} from './patientsApiSlice.jsx'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faSave} from '@fortawesome/free-solid-svg-icons'
import InputAdornment from '@mui/material/InputAdornment';
import TextField from '@mui/material/TextField';

const EMAIL_REGEX = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/
const MOBILENUMBER_REGEX = /^(\+\d{1,3}[- ]?)?\d{10}$/

const NewPatientForm = ({medecin}) => {

    const [addNewPatient, {
        isLoading,
        isSuccess,
        isError,
        error
    }] = useAddNewPatientMutation()

    const navigate = useNavigate()

    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [validid, setvalidid] = useState(false)
    const [address, setAddress] = useState('')
    const [telecom, setTelecom] = useState('')
    const [validtelecom, setValidtelecom] = useState(false)
    const [iserror, setIsError] = useState(false);
    const [medecin_id, setMedecin_id] = useState([medecin[0].id])

    useEffect(() => {
        setvalidid(EMAIL_REGEX.test(email))
    }, [email])

    useEffect(() => {
        setValidtelecom(MOBILENUMBER_REGEX.test(telecom))
    }, [telecom])

    useEffect(() => {
        if (isSuccess) {
            setName('')
            setEmail('')
            setAddress('')
            setTelecom('')
            setMedecin_id('')
            navigate('/dash/patients')
            window.location.reload()
        }

    }, [isSuccess, navigate])

    const onPatientNameChanged = e => setName(e.target.value)
    const onPatientPIDChanged = e => setEmail(e.target.value)
    const onAddressChanged = e => setAddress(e.target.value)
    const onMobileNumberChanged = e => {
        setTelecom(e.target.value)
        if (e.target.value.length > 10) setIsError(true)
    }
    // const onDoctorIDChanged = e => setDoctorID(e.target.value)
    const onDoctorIDChanged = e => {
        const values = Array.from(
            e.target.selectedOptions, //HTMLCollection
            (option) => option.id
        )
        setMedecin_id(values)
    }

    const canSave = [name, email, address, telecom, medecin_id].every(Boolean) && !isLoading

    const onSavePatientClicked = async (e) => {
        e.preventDefault()
        if (canSave && validid && validtelecom) {
            const result = await addNewPatient({
                'email': email,
                'name': name,
                'address': address,
                'telecom': telecom,
                'medecin_id': medecin_id[0]
            })
            if (result.error) {
                alert('Unable to create new patient! please try again...')
            } else {
                alert('New patient created successfully')
            }

        } else if (!validtelecom && !validid) {
            alert('Invalid Email ID and mobile number')
        } else if (!validtelecom) {
            alert('Invalid Mobile Number')
        } else if (!validid) {
            alert('Invalid Email ID')
        } else {
            alert('Unable to create new patient! please try again...')
        }
    }


    const options = medecin.map(user => {
        return (
            <option
                key={user.id}
                value={user.id}
                id={user.id}

            > {user.name} </option>
        )
    })


    const errClass = (isError) ? "errmsg" : "offscreen"
    const errContent = (error?.data?.message) ?? ''

    const content = (
        <>
            <p className={errClass}>{errContent}</p>
            <div>
                <form className="form" onSubmit={e => e.preventDefault()}>
                    <div className="form__title-row">
                        <h2>Add New Patient</h2>
                        <div className="form__action-buttons">
                            <button
                                className="icon-button"
                                title="Save"
                                onClick={onSavePatientClicked}
                                disabled={!canSave}
                            >
                                <FontAwesomeIcon icon={faSave}/>
                            </button>
                        </div>
                    </div>

                    <div className="patient-details-first-row">
                        <div className='patient-details-first-row--first-column'>
                            <div><TextField
                                className='form__input--patient'
                                id="note-title"
                                name="title"
                                type="text"
                                label="Enter Patient Name"
                                autoComplete="off"
                                value={name}
                                onChange={onPatientNameChanged}
                            /></div>


                            <div><TextField
                                className='form__input--patient'
                                id="note-title"
                                name="title"
                                type="text"
                                label="Enter Patient Address"
                                autoComplete="off"
                                value={address}
                                onChange={onAddressChanged}
                            /></div>


                            <div><TextField
                                required
                                className='form__input--patient'
                                id="note-title"
                                name="title"
                                type="tel"
                                label="Enter Patient Mobile Number"
                                autoComplete="off"
                                error={iserror}
                                value={telecom}
                                onChange={onMobileNumberChanged}
                                InputProps={{
                                    startAdornment: <InputAdornment position="start">
                                        +33
                                    </InputAdornment>,
                                }}
                            /></div>
                        </div>

                        <div className='patient-details-first-row--second-column'>


                            <div><TextField
                                className='form__input--patient'
                                id="note-title"
                                name="title"
                                type="text"
                                label="Enter Email ID"
                                autoComplete="off"
                                value={email}
                                onChange={onPatientPIDChanged}
                            /></div>

                            <div className="form__row">
                                <div className="form__divider">
                                    <label className="form__label form__checkbox-container" htmlFor="note-username">
                                        ASSIGNED TO DOCTOR:</label>
                                    <select
                                        id="note-username"
                                        name="username"
                                        className="form__select"
                                        value={medecin_id}
                                        onChange={onDoctorIDChanged}
                                    >
                                        {options}
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>

                </form>
            </div>
        </>
    )

    return content


}

export default NewPatientForm
