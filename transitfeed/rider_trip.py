from problems import default_problem_reporter
from gtfsobjectbase import GtfsObjectBase
import util

class Rider_trip(GtfsObjectBase):
  """This class represents a rule that determines which itineraries a
  fare rule applies to."""
  _REQUIRED_FIELD_NAMES = ['rider_id']
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + [
                                         'trip_id',
                                         'agency_id',
                                         'boarding_stop_id',
                                         'boarding_stop_sequence',
                                         'alighting_stop_id',
                                         'alighting_stop_sequence',
                                         'service_date',
                                         'alighting_time',
                                         'boarding_time',
                                         'rider_type',
                                         'rider_type_description',
                                         'fare_paid',
                                         'transaction_type',
                                         'fare_media',
                                         'accompanying_device',
                                         'transfer_status']
  _TABLE_NAME = "rider_trip"

  def __init__(self,name=None,rider_id = None,trip_id = None,agency_id = None, boarding_stop_id=None, boarding_stop_sequence = None,
    alighting_stop_id=None, alighting_stop_sequence = None, boarding_time=None,
    service_date=None,alighting_time=None,rider_type=None,rider_type_description=None,fare_paid=None, transaction_type = None,
    fare_media=None,accompanying_device=None,transfer_status=None,field_dict=None,**kwargs):
    self._schedule = None

    if not field_dict:
      if rider_id:
        kwargs['rider_id'] = rider_id
      if trip_id:
        kwargs['trip_id'] = trip_id
      if agency_id:
        kwargs['agency_id'] = agency_id
      if boarding_stop_id:
        kwargs['boarding_stop_id'] = boarding_stop_id
      if boarding_stop_sequence:
        kwargs['boarding_stop_sequence'] = boarding_stop_sequence
      if alighting_stop_id:
        kwargs['alighting_stop_id'] = alighting_stop_id
      if alighting_stop_sequence:
        kwargs['alighting_stop_sequence'] = alighting_stop_sequence
      if boarding_time:
        kwargs['boarding_time'] = boarding_time
      if alighting_time:
        kwargs['alighting_time'] = alighting_time
      if service_date:
        kwargs['service_date'] = service_date
      if rider_type:
        kwargs['rider_type'] = rider_type
      if rider_type_description:
        kwargs['rider_type_description'] = rider_type_description
      if fare_paid:
        kwargs['fare_paid'] = fare_paid
      if transaction_type:
        kwargs['transaction_type'] = transaction_type
      if fare_media:
        kwargs['fare_media'] = fare_media
      if accompanying_device:
        kwargs['accompanying_device'] = accompanying_device
      if transfer_status:
        kwargs['transfer_status'] = transfer_status
      field_dict = kwargs
    self.__dict__.update(field_dict)


  def validateBoardingTimeFormat(self,problems):
    if util.IsEmpty(self.boarding_time):
      self.boarding_time = 0
      return
    accept = util.checkInProperTimeFormat(self.boarding_time)
    if accept == 0:
      problems.UnknownTimeFormat('boarding_time',self.boarding_time)

  def validateAlightingTimeFormat(self,problems):
    if util.IsEmpty(self.alighting_time):
      self.alighting_time = 0
      return
    accept = util.checkInProperTimeFormat(self.alighting_time)
    if accept == 0:
      problems.UnknownTimeFormat('alighting_time',self.alighting_time)

  def validateRiderType(self,problems):
    if util.IsEmpty(self.rider_type):
      self.rider_type = 0
      return
    try:
      self.rider_type = int(self.rider_type)
    except (ValueError, TypeError):
      problems.InvalidValue('rider_type', self.rider_type,'Must be integer in range 0 to 13')
      del self.rider_type
      return
    if self.rider_type < 0 or self.rider_type > 13:
      problems.InvalidValue('rider_type', self.rider_type,
          'Must be integer in range 0 to 13')

  def validateFarePaid(self,problems):
    if util.IsEmpty(self.fare_paid):
      self.fare_paid = 0.0
      return
    try:
      self.fare_paid = float(self.fare_paid)
    except (ValueError, TypeError):
      problems.InvalidValue('fare_paid', self.fare_paid,'Must be float amount describing fare amount')
      del self.fare_paid
      return
    if isinstance(self.fare_paid,float)==False:
      problems.InvalidValue('fare_paid', self.fare_paid,
          'Must be float amount describing fare amount')

  def validateFareMedia(self,problems):
    if util.IsEmpty(self.fare_media):
      self.fare_media = 0
      return
    try:
      self.fare_media = int(self.fare_media)
    except (ValueError, TypeError):
      problems.InvalidValue('fare_media', self.fare_media,'Must be integer in range 0 to 9')
      del self.fare_media
      return
    if self.fare_media < 0 or self.fare_media > 9:
      problems.InvalidValue('fare_media', self.fare_media,
          'Must be integer in range 0 to 9')

  def validateAccompanyingDevice(self,problems):
    if util.IsEmpty(self.accompanying_device):
      self.accompanying_device = 0
      return
    try:
      self.accompanying_device = int(self.accompanying_device)
    except (ValueError, TypeError):
      problems.InvalidValue('accompanying_device', self.accompanying_device,'Must be integer in range 0 to 6')
      del self.accompanying_device
      return
    if self.accompanying_device < 0 or self.accompanying_device > 6:
      problems.InvalidValue('accompanying_device', self.accompanying_device,
          'Must be integer in range 0 to 6')

  def validateTransferStatus(self,problems):
    if util.IsEmpty(self.transfer_status):
        self.transfer_status = 0
        return
    try:
      self.transfer_status = int(self.transfer_status)
    except (ValueError, TypeError):
      problems.InvalidValue('transfer_status', self.transfer_status,
          'Value must be 0 or 1')
      del self.transfer_status
      return
    if self.transfer_status not in (0, 1):
      problems.InvalidValue('transfer_status', self.transfer_status,
          'Value must be 0 or 1')

  def validateRiderTypeDescription(self,problems):
    #string description can be very unique and thus no format testing is applied
    pass

  def validateServiceDate(self,problems):
    valid_date = util.ValidateDate(self.service_date,
                                               'service_date', problems)
    if self._schedule.validRideDates == 0:
      return
    if valid_date:
      if self.service_date > self._schedule.ride_feed_date[1] or self.service_date < self._schedule.ride_feed_date[0]:
        problems.InvalidValue('service_date',self.service_date,'Service date does not fall in valid range')

  def validateTransactionType(self,problems):
    if util.IsEmpty(self.transaction_type):
      self.transaction_type = 0
      return
    try:
      self.transaction_type = int(self.transaction_type)
    except (ValueError, TypeError):
      problems.InvalidValue('transaction_type', self.transaction_type,'Must be integer in range 0 to 8')
      del self.transaction_type
      return
    if self.transaction_type < 0 or self.transaction_type > 8:
      problems.InvalidValue('transaction_type', self.transaction_type,
          'Must be integer in range 0 to 8')

  def validateAgencyID(self,problems):
    if util.IsEmpty(self.agency_id):
        return
    if self.agency_id not in self._schedule._agencies.keys():
      problems.InvalidValue('agency_id',self.agency_id,'Did not find a matching agency_id in agencies.txt')

  def validateTripID(self,problems):
    if util.IsEmpty(self.trip_id):
        return
    if self.trip_id not in self._schedule.trips.keys():
      problems.InvalidValue('trip_id',self.trip_id,'Did not find a matching trip_id in trips.txt')

  def validateBoardingStopID(self,problems):
    if util.IsEmpty(self.boarding_stop_id):
        return
    if self.boarding_stop_id not in self._schedule.stops.keys():
      problems.InvalidValue('boarding_stop_id',self.trip_id,'Did not find a matching stop_id in stops.txt')

  def validateAlightingStopID(self,problems):
    if util.IsEmpty(self.alighting_stop_id):
        return
    if self.alighting_stop_id not in self._schedule.stops.keys():
      problems.InvalidValue('alighting_stop_id',self.trip_id,'Did not find a matching stop_id in stops.txt')

  def validateBoardingStopSequence(self,problems):
    if util.IsEmpty(self.boarding_stop_sequence):
        return
    if self.boarding_stop_sequence not in self._schedule.stop_sequences:
      problems.InvalidValue('boarding_stop_sequence',self.boarding_stop_sequence,'Did not find a matching stop_sequence in stop_times.txt')

  def validateAlightingStopSequence(self,problems):
    if util.IsEmpty(self.alighting_stop_sequence):
        return
    if self.alighting_stop_sequence not in self._schedule.stop_sequences:
      problems.InvalidValue('alighting_stop_sequence',self.alighting_stop_sequence,'Did not find a matching stop_sequence in stop_times.txt')

  def Validate(self, problems=default_problem_reporter):
    """Validate attribute values and this object's internal consistency.

    Returns:
      True iff all validation checks passed.
    """
    found_problem = False
    found_problem = ((not util.ValidateRequiredFieldsAreNotEmpty(
                          self, self._REQUIRED_FIELD_NAMES, problems))
                          or found_problem)
    found_problem = self.validateBoardingTimeFormat(problems)
    found_problem = self.validateAlightingTimeFormat(problems)
    found_problem = self.validateRiderType(problems)
    found_problem = self.validateFarePaid(problems)
    found_problem = self.validateFareMedia(problems)
    found_problem = self.validateAccompanyingDevice(problems)
    found_problem = self.validateTransferStatus(problems)
    found_problem = self.validateServiceDate(problems)
    found_problem = self.validateTransactionType(problems)
    found_problem = self.validateAgencyID(problems)
    found_problem = self.validateTripID(problems)
    found_problem = self.validateBoardingStopID(problems)
    found_problem = self.validateAlightingStopID(problems)
    found_problem = self.validateAlightingStopSequence(problems)
    found_problem = self.validateBoardingStopSequence(problems)
    found_problem = self.validateRiderTypeDescription(problems)



    return not found_problem

  def ValidateBeforeAdd(self, problems):
    return True

  def ValidateAfterAdd(self, problems):
    self.Validate(problems)
    return