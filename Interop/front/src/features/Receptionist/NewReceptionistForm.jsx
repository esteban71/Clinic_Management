import React, {useEffect, useState} from 'react'
import {useAddNewReceptionistMutation} from './ReceptionistApiSlice.jsx'
import {useNavigate} from 'react-router-dom'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faSave} from '@fortawesome/free-solid-svg-icons'
import useAuth from '../../hooks/useAuth.jsx'
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';

const USER_REGEX = /^[A-z0-9]{3,20}$/
const PWD_REGEX = /^[A-z0-9!@#$%]{4,12}$/
const MOBILENUMBER_REGEX = /^(\+\d{1,3}[- ]?)?\d{10}$/

const NewReceptionistForm = ({cabinet}) => {
    const {isManager, isAdmin, isReceptionist} = useAuth()

    const [addNewReceptionist, {isLoading, isSuccess, isError, error}] = useAddNewReceptionistMutation();

    const navigate = useNavigate()

    const [name, setName] = useState('')
    const [mobileNumber, setMobileNumber] = useState('')
    const [validMobileNumber, setValidMobileNumber] = useState(false)
    const [username, setUsername] = useState('')
    const [validUsername, setValidUsername] = useState(false)
    const [email, setEmail] = useState('')
    const [validEmail, setValidEmail] = useState(false)
    const [cabinet_id, setCabinetId] = useState([cabinet[0].id])
    const [validCabinetId, setValidCabinetId] = useState(false)
    const [password, setPassword] = useState('')
    const [reEnterPassword, setReEnterPassword] = useState('')
    const [validPassword, setValidPassword] = useState(false)
    const [iserror, setIsError] = useState(false);
    const [values, setValues] = React.useState({
        password: "",
        showPassword: false,
    });

    const handleClickShowPassword = () => {
        setValues({...values, showPassword: !values.showPassword});
    };

    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };

    const handlePasswordChange = (prop) => (event) => {
        setValues({...values, [prop]: event.target.value});
    };

    useEffect(() => {
        setValidUsername(USER_REGEX.test(username))
    }, [username])

    useEffect(() => {
        setValidMobileNumber(MOBILENUMBER_REGEX.test(mobileNumber))
    }, [mobileNumber])

    useEffect(() => {
        setValidPassword(PWD_REGEX.test(values.password))
    }, [values.password])

    useEffect(() => {
        if (isSuccess) {
            setName('')
            setMobileNumber('')
            setUsername('')
            setEmail('')
            setPassword('')
            setReEnterPassword('')
            setCabinetId([])
            navigate('/dash/receptionists')
            window.location.reload()
        }
    }, [isSuccess, navigate])

    const onNameChanged = e => setName(e.target.value)
    const onMobileNumberChanged = e => setMobileNumber(e.target.value)
    const onUsernameChanged = e => setUsername(e.target.value)
    const onPasswordChanged = e => setPassword(e.target.value)
    const onReEnterPassword = e => setReEnterPassword(e.target.value)
    const onEmailChanged = e => setEmail(e.target.value)
    const onCabinetIdChanged = e => {
        const values = Array.from(
            e.target.selectedOptions,
            (option) => option.id
        )
        setCabinetId(values)
    }


    const canSave = [name, mobileNumber, username, email, values.password, cabinet_id.length].every(Boolean) && !isLoading

    const onSaveUserClicked = async (e) => {
        e.preventDefault()
        if (canSave && validUsername && validPassword && validMobileNumber && (values.password === reEnterPassword)) {
            const result = await addNewReceptionist({
                'name': name,
                'telecom': mobileNumber,
                'username': username,
                'email': email,
                password: values.password,
                "cabinet_id": cabinet_id[0]
            })
            if (result.error) {
                alert('Unable to create new Doctor! please try again...')
            } else {
                alert('New Receptionist created successfully')
            }

        } else if (!validUsername && !validPassword && !validMobileNumber && !(values.password === reEnterPassword)) {
            alert('All fields are invalid')
        } else if (!validUsername) {
            alert('Invalid username')
        } else if (!validPassword) {
            alert('Invalid password')
        } else if (!validMobileNumber) {
            alert('Invalid mobile number')
        } else if (!(values.password === reEnterPassword)) {
            alert('Please re-enter password correctly')
        } else {
            alert('Unable to create new Doctor! please try again...')
        }
    }

    const cabinetOptions = Object.values(cabinet).map(cabinet => {
        return (
            <option
                key={cabinet.id}
                value={cabinet.id}
                id={cabinet.id}
            > {cabinet.name}</option>
        )
    })


    const errClass = isError ? "errmsg" : "offscreen"


    const content = (
        <>
            <p className={errClass}>{error?.data?.message}</p>

            <form className="form" onSubmit={onSaveUserClicked}>
                <div className="form__title-row">
                    <h2>Add New Receptionist</h2>
                    <div className="form__action-buttons">
                        <button
                            className="icon-button"
                            title="Save"
                            disabled={!canSave}
                        >
                            <FontAwesomeIcon icon={faSave}/>
                        </button>
                    </div>
                </div>

                <TextField
                    className={`form__input`}
                    id="name"
                    name="name"
                    type="text"
                    label="Enter Receptionist's name"
                    autoComplete="on"
                    value={name}
                    onChange={onNameChanged}
                />

                <TextField
                    required
                    className='form__input--patient'
                    id="note-title"
                    name="title"
                    type="tel"
                    label="Enter Receptionist Mobile Number"
                    autoComplete="off"
                    error={iserror}
                    value={mobileNumber}
                    onChange={onMobileNumberChanged}
                    InputProps={{
                        startAdornment: <InputAdornment position="start">
                            +33
                        </InputAdornment>,
                    }}
                />

                <TextField
                    className={`form__input`}
                    id="username"
                    name="username"
                    type="text"
                    label=" Enter Receptionist's username"
                    autoComplete="off"
                    value={username}
                    onChange={onUsernameChanged}
                />

                <TextField
                    className={`form__input`}
                    id="email"
                    name="email"
                    type="text"
                    label=" Enter email"
                    autoComplete="off"
                    value={email}
                    onChange={onEmailChanged}
                />

                <TextField
                    className={`form__input`}
                    id="password"
                    name="password"
                    label=" Enter password"
                    type={values.showPassword ? "text" : "password"}
                    value={values.password}
                    onChange={handlePasswordChange("password")}
                    InputProps={{
                        endAdornment: <InputAdornment position="end">
                            <IconButton
                                onClick={handleClickShowPassword}
                                onMouseDown={handleMouseDownPassword}
                            >
                                {values.showPassword ? <Visibility/> : <VisibilityOff/>}
                            </IconButton>
                        </InputAdornment>
                    }}
                />

                <TextField
                    className={`form__input`}
                    id="ReEnterPassword"
                    name="ReEnterPassword"
                    type="password"
                    label=" Re-Enter password"
                    value={reEnterPassword}
                    onChange={onReEnterPassword}
                />

                <label className="form__label form__checkbox-container" htmlFor="cabinet">
                    ASSIGNED CABINET:</label>
                <select
                    id="cabinet"
                    name="cabinet"
                    className="form__select"
                    value={cabinet_id}

                    onChange={onCabinetIdChanged}
                >

                    {cabinetOptions}
                </select>

            </form>
        </>
    )

    return content

}

export default NewReceptionistForm

