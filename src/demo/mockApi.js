const demoLogo = `data:image/svg+xml,${encodeURIComponent(`
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 64">
  <rect width="240" height="64" rx="14" fill="#ffffff"/>
  <circle cx="32" cy="32" r="22" fill="#1f9d87"/>
  <path d="M22 32h20M32 22v20" stroke="#fff" stroke-width="6" stroke-linecap="round"/>
  <text x="64" y="40" font-family="Arial,sans-serif" font-size="25" font-weight="700" fill="#1f2937">Marley Health</text>
</svg>
`)}`

const today = () => new Date().toISOString().slice(0, 10)
const nowTime = () => new Date().toTimeString().slice(0, 5)
const option = (label, value = label) => ({ label, value })

const practitioners = [
  option('Dr. Sara Nasser', 'HPR-0001'),
  option('Dr. Omar Kareem', 'HPR-0002'),
  option('Dr. Lina Hassan', 'HPR-0003'),
  option('Dr. David Joseph', 'HPR-0004'),
]

const departments = [
  option('Psychiatry'),
  option('General Medicine'),
  option('Neurology'),
  option('Cardiology'),
]

const patients = [
  { name: 'PAT-0001', patient_name: 'Layla Ahmed', mobile: '07701234567', sex: 'Female', age: 29 },
  { name: 'PAT-0002', patient_name: 'Ali Hassan', mobile: '07812345678', sex: 'Male', age: 41 },
  { name: 'PAT-0003', patient_name: 'Noor Abbas', mobile: '07504561234', sex: 'Female', age: 36 },
  { name: 'PAT-0004', patient_name: 'Mustafa Kareem', mobile: '07719876543', sex: 'Male', age: 52 },
  { name: 'PAT-0005', patient_name: 'Zahraa Mohammed', mobile: '07805551234', sex: 'Female', age: 24 },
  { name: 'PAT-0006', patient_name: 'Haidar Salman', mobile: '07511223344', sex: 'Male', age: 63 },
]

function appointment({ id, patientIndex, practitionerIndex, department, type, time, status, token, tokenStatus = 'Active', encounter = null, reason = '' }) {
  const p = patients[patientIndex]
  const pr = practitioners[practitionerIndex]
  return {
    name: id,
    title: `${p.patient_name} — ${pr.label}`,
    patient: p.name,
    patient_id: p.name,
    patient_name: p.patient_name,
    mobile: p.mobile,
    image: null,
    practitioner: pr.value,
    practitioner_name: pr.label,
    practitioner_image: null,
    department,
    appointment_type: type,
    appointment_date: today(),
    booked_time: time,
    appointment_time: `${time}:00`,
    checkin_time: ['Checked In', 'Attending', 'Checked Out', 'Consulted'].includes(status) ? time : '',
    patient_token_number: token || '',
    token_no: token || '',
    token_status: tokenStatus,
    token_su_name: token ? `${department} Queue` : '',
    status,
    statusClass: status === 'Cancelled' ? '!text-red-600' : status === 'Consulted' ? '!text-green-600' : status === 'Checked In' ? '!text-blue-600' : '',
    consulted: status === 'Consulted',
    has_token: Boolean(token),
    has_encounter: Boolean(encounter),
    encounter,
    custom_cancel_reason: status === 'Cancelled' ? reason || 'Patient requested cancellation' : '',
    custom_reschedule_reason: '',
    custom_registration_fee_paid: ['Confirmed', 'Checked In', 'Attending', 'Checked Out', 'Consulted'].includes(status),
    custom_consultation_paid: ['Checked In', 'Attending', 'Checked Out', 'Consulted'].includes(status),
    registration_fee: 10000,
    consultation_fee: 25000,
    invoiced: ['Checked In', 'Attending', 'Checked Out', 'Consulted'].includes(status),
  }
}

const state = {
  appointments: [
    appointment({ id: 'APT-0001', patientIndex: 0, practitionerIndex: 0, department: 'Psychiatry', type: 'Initial Consultation', time: '09:00', status: 'Checked In', token: 'P-12' }),
    appointment({ id: 'APT-0002', patientIndex: 1, practitionerIndex: 1, department: 'General Medicine', type: 'Follow-up', time: '09:30', status: 'Confirmed', token: 'G-07' }),
    appointment({ id: 'APT-0003', patientIndex: 2, practitionerIndex: 2, department: 'Neurology', type: 'Initial Consultation', time: '10:00', status: 'Scheduled' }),
    appointment({ id: 'APT-0004', patientIndex: 3, practitionerIndex: 3, department: 'Cardiology', type: 'Follow-up', time: '10:30', status: 'Attending', token: 'C-04', encounter: 'ENC-0004' }),
    appointment({ id: 'APT-0005', patientIndex: 4, practitionerIndex: 0, department: 'Psychiatry', type: 'Psychotherapy', time: '11:00', status: 'Open' }),
    appointment({ id: 'APT-0006', patientIndex: 5, practitionerIndex: 1, department: 'General Medicine', type: 'Follow-up', time: '11:30', status: 'Consulted', token: 'G-11', encounter: 'ENC-0006' }),
    appointment({ id: 'APT-0007', patientIndex: 1, practitionerIndex: 2, department: 'Neurology', type: 'Initial Consultation', time: '12:00', status: 'Cancelled', reason: 'Travel conflict' }),
    appointment({ id: 'APT-0008', patientIndex: 3, practitionerIndex: 0, department: 'Psychiatry', type: 'Follow-up', time: '12:30', status: 'No Show' }),
    appointment({ id: 'APT-0009', patientIndex: 0, practitionerIndex: 3, department: 'Cardiology', type: 'Initial Consultation', time: '13:00', status: 'Checked Out', token: 'C-09', encounter: 'ENC-0009' }),
  ],
  rooms: [
    {
      room_type_details: 'General Ward',
      rooms: [
        { name: 'BED-G-01', healthcare_service_unit_name: 'General 01', room_status: 'Occupied', rate: 75000, uom: 'Day', patient: 'PAT-0004', patient_name: 'Mustafa Kareem', admission_encounter: 'ENC-0104', primary_practitioner: 'Dr. Omar Kareem', ip_record: 'IPD-0004', ip_status: 'Admitted', check_in: `${today()} 08:10:00`, admission_ordered_for: today(), expected_discharge: today(), admitted_datetime: `${today()} 08:25:00`, discharge_datetime: '', disable_schedule: false },
        { name: 'BED-G-02', healthcare_service_unit_name: 'General 02', room_status: 'Vacant', rate: 75000, uom: 'Day', ip_status: '', disable_schedule: false },
        { name: 'BED-G-03', healthcare_service_unit_name: 'General 03', room_status: 'Cleaning', rate: 75000, uom: 'Day', ip_status: '', disable_schedule: false },
        { name: 'BED-G-04', healthcare_service_unit_name: 'General 04', room_status: 'Under Maintenance', rate: 75000, uom: 'Day', ip_status: '', disable_schedule: false },
      ],
    },
    {
      room_type_details: 'Private Rooms',
      rooms: [
        { name: 'BED-P-01', healthcare_service_unit_name: 'Private 01', room_status: 'Vacant', rate: 150000, uom: 'Day', ip_status: '', disable_schedule: false },
        { name: 'BED-P-02', healthcare_service_unit_name: 'Private 02', room_status: 'Occupied', rate: 150000, uom: 'Day', patient: 'PAT-0006', patient_name: 'Haidar Salman', admission_encounter: 'ENC-0106', primary_practitioner: 'Dr. David Joseph', ip_record: 'IPD-0006', ip_status: 'Admitted', check_in: `${today()} 07:45:00`, admission_ordered_for: today(), expected_discharge: today(), admitted_datetime: `${today()} 08:00:00`, discharge_datetime: '', disable_schedule: false },
        { name: 'BED-P-03', healthcare_service_unit_name: 'Private 03', room_status: 'Vacant', rate: 150000, uom: 'Day', ip_status: '', disable_schedule: false },
      ],
    },
    {
      room_type_details: 'ICU',
      rooms: [
        { name: 'BED-I-01', healthcare_service_unit_name: 'ICU 01', room_status: 'Occupied', rate: 300000, uom: 'Day', patient: 'PAT-0002', patient_name: 'Ali Hassan', admission_encounter: 'ENC-0202', primary_practitioner: 'Dr. David Joseph', ip_record: 'IPD-0202', ip_status: 'Admitted', check_in: `${today()} 04:20:00`, admission_ordered_for: today(), expected_discharge: today(), admitted_datetime: `${today()} 04:40:00`, discharge_datetime: '', disable_schedule: false },
        { name: 'BED-I-02', healthcare_service_unit_name: 'ICU 02', room_status: 'Vacant', rate: 300000, uom: 'Day', ip_status: '', disable_schedule: false },
      ],
    },
  ],
}

const serviceUnits = [option('Psychiatry Queue', 'SU-PSY'), option('General Medicine Queue', 'SU-GM'), option('Neurology Queue', 'SU-NEU'), option('Cardiology Queue', 'SU-CAR')]

const settings = {
  doctype: 'Marley Frontend Settings',
  name: 'Marley Frontend Settings',
  brand_name: 'Marley Health Demo',
  brand_logo: demoLogo,
  favicon: demoLogo,
  home_screen_brand: demoLogo,
  show_browser_alert_for_otp: 1,
  show_qr_camera_on_checkin_page: 0,
  show_qr_camera_on_kiosk_page: 0,
  default_appointment_type: 'Initial Consultation',
  dropdown_items: [
    { name1: 'toggle_theme', label: 'Toggle theme', icon: 'moon', type: 'Item', is_standard: 1, hidden: 0 },
    { name1: 'about', label: 'About Marley', icon: 'info', type: 'Item', is_standard: 1, hidden: 0 },
  ],
}

function groupAppointments() {
  const grouped = { All: state.appointments, Open: [], Scheduled: [], Confirmed: [], 'Checked In': [], Attending: [], 'Checked Out': [], Consulted: [], Cancelled: [], 'No Show': [] }
  for (const item of state.appointments) if (grouped[item.status]) grouped[item.status].push(item)
  return grouped
}

function flattenRooms() { return state.rooms.flatMap((group) => group.rooms) }
function paramsFor(options) { return options?.params || {} }
function endpointFor(url = '') { return String(url).replace(/^https?:\/\/[^/]+/, '').replace(/^\/api\/method\//, '').replace(/^\/+/, '') }
function findRoom(name) { return flattenRooms().find((room) => room.name === name) }
function mutateRoom(name, status) { const room = findRoom(name); if (room) room.room_status = status; return room }

function tokenPayload(serviceUnit) {
  const maps = {
    'SU-PSY': { service_unit_name: 'Psychiatry', practitioner: 'Dr. Sara Nasser', results: [{ token_no: 'P-12', status: 'In Progress', isBlinking: false }, { token_no: 'P-13', status: 'Waiting', isBlinking: false }, { token_no: 'P-14', status: 'Waiting', isBlinking: false }] },
    'SU-GM': { service_unit_name: 'General Medicine', practitioner: 'Dr. Omar Kareem', results: [{ token_no: 'G-07', status: 'In Progress', isBlinking: false }, { token_no: 'G-08', status: 'Waiting', isBlinking: false }, { token_no: 'G-09', status: 'Waiting', isBlinking: false }] },
    'SU-NEU': { service_unit_name: 'Neurology', practitioner: 'Dr. Lina Hassan', results: [{ token_no: 'N-03', status: 'In Progress', isBlinking: false }, { token_no: 'N-04', status: 'Waiting', isBlinking: false }, { token_no: 'N-05', status: 'Waiting', isBlinking: false }] },
    'SU-CAR': { service_unit_name: 'Cardiology', practitioner: 'Dr. David Joseph', results: [{ token_no: 'C-04', status: 'In Progress', isBlinking: false }, { token_no: 'C-05', status: 'Waiting', isBlinking: false }, { token_no: 'C-06', status: 'Waiting', isBlinking: false }] },
  }
  return { ...(maps[serviceUnit] || maps['SU-PSY']), number_of_rows: 3 }
}

function success(message = 'Demo action completed') { return { status: 'success', success: true, message } }

export function seedPreviewGlobals() {
  window.__MARLEY_AI_STUDIO_PREVIEW__ = true
  window.timezone = window.timezone || { system: 'Asia/Baghdad', user: 'Asia/Baghdad' }
  window.site_name = 'Marley AI Studio Demo'
  window.user = 'demo@marley.local'
  window.user_type = 'System User'
  window.is_system_user = true
  window.sysdefaults = window.sysdefaults || { country: 'Iraq', currency: 'IQD' }
  localStorage.setItem('patient_id', localStorage.getItem('patient_id') || 'PAT-0001')
  localStorage.setItem('patient_name', localStorage.getItem('patient_name') || 'Layla Ahmed')
}

export async function mockResourceFetcher(options = {}) {
  const endpoint = endpointFor(options.url)
  const params = paramsFor(options)
  await new Promise((resolve) => setTimeout(resolve, 80))

  if (endpoint === 'login') return { default_route: '/' }
  if (endpoint === 'logout') return success('Signed out in demo mode')

  if (endpoint === 'frappe.client.get') {
    if (params.doctype === 'Marley Frontend Settings') return settings
    return { doctype: params.doctype, name: params.name, ...params }
  }
  if (endpoint === 'frappe.client.set_value') return { ...params.fieldname, doctype: params.doctype, name: params.name }
  if (endpoint === 'frappe.client.delete') return success()
  if (endpoint === 'run_doc_method') return { message: success(), docs: [] }

  if (endpoint === 'marley_frontend.api.get_user_info') return [{ name: 'demo@marley.local', email: 'demo@marley.local', full_name: 'Demo Administrator', enabled: 1, role: 'System Manager', user_image: null }]
  if (endpoint === 'marley_frontend.api.get_logo_image' || endpoint === 'marley_frontend.api.get_brand_image') return demoLogo
  if (endpoint === 'marley_frontend.api.get_gender') return { genders: [option('Female'), option('Male'), option('Non-binary'), option('Prefer not to say')] }
  if (endpoint === 'marley_frontend.api.get_departments') return { practitioners, departments, defAppType: 'Initial Consultation' }
  if (endpoint === 'marley_frontend.api.get_practitioners') return practitioners
  if (endpoint === 'marley_frontend.api.get_slots' || endpoint === 'marley_frontend.waitlist.get_slots_in_dialog') return { slots: ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '13:00', '13:30', '14:00', '15:00'] }
  if (endpoint === 'marley_frontend.api.get_patient') return { status: 'success', patients: patients.slice(0, 3) }
  if (endpoint === 'marley_frontend.api.send_otp') return { status: 'Success', alert: true, message: `Demo OTP: ${params.otp || '123456'}` }

  if (endpoint === 'marley_frontend.api.get_current_patient_data' || endpoint === 'marley_frontend.api.check_patient_details') {
    const p = patients.find((item) => item.name === (params.patient || params.patient_id)) || patients[0]
    return { profile_completed: true, status: 'success', doc: { name: p.name, first_name: p.patient_name.split(' ')[0], last_name: p.patient_name.split(' ').slice(1).join(' '), sex: p.sex, mobile: p.mobile, dob: '1997-05-14', address_line1: 'Karbala City Center', address_line2: '', city: 'Karbala', state: 'Karbala', zip_code: '', marital_status: 'Single' } }
  }

  if (endpoint === 'marley_frontend.api.update_patient') return success('Patient profile updated')
  if (endpoint === 'marley_frontend.api.get_patient_appointment') {
    const patient = params.patient || 'PAT-0001'
    const appt = state.appointments.find((item) => item.patient_id === patient && item.status !== 'Cancelled')
    return appt?.name || null
  }

  if (endpoint === 'marley_frontend.api.patient_registration') {
    const id = `PAT-${String(patients.length + 1).padStart(4, '0')}`
    const patientName = `${params.first_name || 'Demo'} ${params.last_name || 'Patient'}`.trim()
    patients.push({ name: id, patient_name: patientName, mobile: params.mobile || '07700000000', sex: params.gender || 'Female', age: Number(params.age || 30) })
    localStorage.setItem('patient_id', id)
    localStorage.setItem('patient_name', patientName)
    return { status: 'success', patient: id, patient_name: patientName }
  }

  if (endpoint === 'marley_frontend.api.patient_appointment') {
    const id = `APT-${String(state.appointments.length + 1).padStart(4, '0')}`
    const patientId = params.patient || localStorage.getItem('patient_id') || 'PAT-0001'
    const patientIndex = Math.max(0, patients.findIndex((p) => p.name === patientId))
    const practitionerIndex = Math.max(0, practitioners.findIndex((p) => p.value === params.practitioner))
    const item = appointment({ id, patientIndex, practitionerIndex, department: params.department || 'Psychiatry', type: params.appointment_type || 'Initial Consultation', time: params.time || params.appointment_time || '14:30', status: 'Scheduled' })
    item.appointment_date = params.date || params.appointment_date || today()
    state.appointments.push(item)
    return { status: 'success', name: id }
  }

  if (endpoint === 'marley_frontend.api.get_units') return serviceUnits
  if (endpoint === 'marley_frontend.api.get_tokens') return tokenPayload(params.service_unit)
  if (endpoint === 'marley_frontend.api.get_file') return 'data:text/plain,Marley%20Health%20Demo%20%E2%80%94%20Queue%20Display'

  if (endpoint === 'marley_frontend.waitlist.get_appointments') return groupAppointments()
  if (endpoint === 'marley_frontend.waitlist.get_default_appointment') return 'Initial Consultation'

  if (endpoint === 'marley_frontend.waitlist.set_status') {
    const item = state.appointments.find((appt) => appt.name === (params.id || params.appointment))
    if (item && params.status) item.status = params.status
    return success(`Appointment moved to ${params.status || 'new status'}`)
  }

  if (endpoint === 'marley_frontend.waitlist.get_vitals') return { height: 171, weight: 72, temperature: 36.8, pulse: 78, respiratory_rate: 16, bp_systolic: 118, bp_diastolic: 76, oxygen_saturation: 98 }
  if (endpoint === 'marley_frontend.waitlist.create_vitalsigns') return { status: 'success', name: 'VITAL-DEMO-001' }
  if (endpoint === 'marley_frontend.waitlist.submit_vitalsigns') return success('Vitals submitted')

  if (endpoint === 'marley_frontend.waitlist.reschedule_appointment_booking') {
    const item = state.appointments.find((appt) => appt.name === (params.appointment_id || params.appointment))
    if (item) { item.appointment_date = params.appointment_date || item.appointment_date; item.booked_time = params.appointment_time || params.time || item.booked_time; item.status = 'Scheduled'; item.custom_reschedule_reason = params.reason || 'Rescheduled in demo' }
    return success('Appointment rescheduled')
  }

  if (endpoint === 'marley_frontend.waitlist.get_patient_data_for_services') return { patient: patients[0].name, patient_name: patients[0].patient_name, customer: option(patients[0].patient_name, 'CUST-0001'), company: option('Marley Demo Hospital'), encounter: 'ENC-DEMO-001' }
  if (endpoint === 'marley_frontend.waitlist.get_service_list') return [{ item_code: 'LAB-CBC', item_name: 'Complete Blood Count', rate: 15000, qty: 1 }, { item_code: 'ECG', item_name: 'ECG', rate: 20000, qty: 1 }, { item_code: 'CONSULT', item_name: 'Consultation', rate: 25000, qty: 1 }]
  if (endpoint === 'marley_frontend.waitlist.get_prescriptions') return [{ item_code: 'MED-001', item_name: 'Demo Medicine A', qty: 1, rate: 5000 }, { item_code: 'MED-002', item_name: 'Demo Medicine B', qty: 2, rate: 3500 }]
  if (endpoint === 'marley_frontend.waitlist.get_mode_of_payments') return [option('Cash'), option('Card'), option('Bank Transfer')]
  if (endpoint === 'marley_frontend.waitlist.fetch_mode_type') return params.mode === 'Cash' ? 'Cash' : 'Bank'
  if (endpoint === 'marley_frontend.waitlist.get_boarding_pass_print_format') return 'Standard'
  if (endpoint === 'marley_frontend.waitlist.create_services_sales_invoice' || endpoint === 'marley_frontend.waitlist.create_prescription_sales_invoice') return { status: 'success', invoice: 'SINV-DEMO-001' }

  if (endpoint === 'marley_frontend.bed_management.get_filter_options') {
    const rooms = flattenRooms()
    return { type_options: state.rooms.map((group) => option(group.room_type_details)), service_unit_options: rooms.map((room) => option(room.healthcare_service_unit_name, room.name)), patient_options: patients.map((p) => option(p.patient_name, p.name)), allocate_patient_options: patients.map((p) => option(p.patient_name, p.name)), consultant_options: practitioners }
  }

  if (endpoint === 'marley_frontend.bed_management.get_room_details') {
    const groups = state.rooms.map((group) => ({ ...group, rooms: group.rooms.filter((room) => { if (params.room_type_filter && group.room_type_details !== params.room_type_filter) return false; if (params.bed_filter && room.name !== params.bed_filter) return false; if (params.patient_filter && room.patient !== params.patient_filter) return false; if (params.status_filter && room.room_status !== params.status_filter) return false; return true }) }))
    return groups.filter((group) => group.rooms.length)
  }

  if (endpoint === 'marley_frontend.bed_management.get_filter_room') {
    const group = state.rooms.find((item) => !params.room_type || item.room_type_details === params.room_type)
    return (group?.rooms || []).filter((room) => room.room_status === 'Vacant').map((room) => option(room.healthcare_service_unit_name, room.name))
  }

  if (endpoint === 'marley_frontend.bed_management.get_encounter_options') return [option('ENC-DEMO-101'), option('ENC-DEMO-102'), option('ENC-DEMO-103')]
  if (endpoint === 'marley_frontend.bed_management.change_status') { mutateRoom(params.room, params.status || 'Vacant'); return success(`Room marked ${params.status || 'Vacant'}`) }

  if (endpoint === 'marley_frontend.bed_management.order_admission') {
    const room = findRoom(params.service_unit || params.bed || params.room)
    if (room) { room.patient = params.patient || 'PAT-0001'; room.patient_name = patients.find((p) => p.name === room.patient)?.patient_name || 'Demo Patient'; room.ip_status = 'Admission Scheduled'; room.ip_record = 'IPD-DEMO-101'; room.admission_encounter = params.encounter || 'ENC-DEMO-101'; room.primary_practitioner = params.primary_practitioner || 'Dr. Sara Nasser' }
    return success('Admission scheduled')
  }

  if (endpoint === 'marley_frontend.bed_management.admit_patient') {
    const room = findRoom(params.service_unit)
    if (room) { room.room_status = 'Occupied'; room.ip_status = 'Admitted'; room.admitted_datetime = `${today()} ${nowTime()}:00`; room.check_in = room.admitted_datetime }
    return success('Patient admitted')
  }

  if (endpoint === 'marley_frontend.bed_management.order_bed_transfer') return success('Bed transfer completed in demo')
  if (endpoint === 'marley_frontend.api.new_error_log') return success('Demo log ignored')
  if (endpoint.includes('frappe.client.get_list') || endpoint.includes('frappe.client.get_all')) return []
  if (endpoint.includes('frappe.client.get_value')) return {}
  if (endpoint.startsWith('api/resource/') || endpoint.startsWith('resource/')) return []
  if (endpoint.startsWith('marley_frontend.')) return success()

  console.info('[Marley demo] Mocked unknown resource:', endpoint, params)
  return {}
}

export const demoState = state
