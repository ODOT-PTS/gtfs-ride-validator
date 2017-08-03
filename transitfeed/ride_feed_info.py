from problems import default_problem_reporter
from gtfsobjectbase import GtfsObjectBase
import util

class Ride_feed_info(GtfsObjectBase):
  """This class represents a rule that determines which itineraries a
  fare rule applies to."""
  _REQUIRED_FIELD_NAMES = ['ride_files']
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + [
                                         'ride_start_date',
                                         'ride_end_date',
                                         'gtfs_feed_date',
                                         'default_currency_type',
                                         'ride_feed_version']
  _TABLE_NAME = "ride_feed_info"

  def __init__(self,name=None,ride_files = None,ride_start_date = None,ride_end_date = None,gtfs_feed_date=None,
                default_currency_type=None, ride_feed_version = None,field_dict=None,**kwargs):
    self._schedule = None
    self.validRideDates = 1

    if not field_dict:
      if ride_files:
        kwargs['ride_files'] = ride_files
      if ride_start_date:
        kwargs['ride_start_date'] = ride_start_date
      if ride_end_date:
        kwargs['ride_end_date'] = ride_end_date
      if gtfs_feed_date:
        kwargs['gtfs_feed_date'] = gtfs_feed_date
      if default_currency_type:
        kwargs['default_currency_type'] = default_currency_type
      if ride_feed_version:
        kwargs['ride_feed_version'] = ride_feed_version
      field_dict = kwargs
    self.__dict__.update(field_dict)


  def validateRideFiles(self,problems):
    if util.IsEmpty(self.ride_files):
      self.ride_files = 0
      return
    try:
      self.ride_files = int(self.ride_files)
    except (ValueError, TypeError):
      problems.InvalidValue('ride_files', self.ride_files,'Must be 0,1,2,3,4,5,6')
      del self.ride_files
      return
    if self.ride_files not in (0,1,2,3,4,5,6):
      problems.InvalidValue('ride_files', self.ride_files,
          'Must be 0,1,2,3,4,5,6')

  def validateCurrencyType(self,problems):
    if util.IsEmpty(self.default_currency_type):
      self.default_currency_type = 0
      return
    try:
      self.default_currency_type = str(self.default_currency_type)
    except (ValueError, TypeError):
      problems.InvalidValue('default_currency_type', self.default_currency_type,'Must be three capital letters')
      del self.default_currency_type
      return
    if len(self.default_currency_type) != 3 or self.default_currency_type.isupper() == False:
      problems.InvalidValue('default_currency_type', self.default_currency_type,
          'Must be three capital letters')
    

  def validateRideStartdate(self,problems):
    if util.IsEmpty(self.ride_start_date):
      self.ride_start_date = "na"
      return
    start_date_valid = util.ValidateDate(self.ride_start_date,
                                               'ride_start_date', problems)
    if start_date_valid == False:
      self.ride_start_date = "na"
      
    
  
  def validateRideDateRanges(self,problems):
    if self._schedule.validDates == 0 or self.ride_start_date == "na":
      return
    else:
      if self.ride_start_date > self._schedule.feed_info.feed_end_date or self.ride_start_date < self._schedule.feed_info.feed_start_date:
        problems.InvalidValue('ride_start_date',self.ride_start_date,'Value not in valid date range according to gtfs feed start and end dates')
    if self.ride_end_date == "na":
      return
    if self.ride_end_date < self._schedule.feed_info.feed_start_date or self.ride_end_date > self._schedule.feed_info.feed_end_date:
      problems.InvalidValue('ride_end_date',self.ride_start_date,'Value not in valid date range according to gtfs feed start and end dates')


  def validateRideEnddate(self,problems):
    if util.IsEmpty(self.ride_end_date):
      self.ride_end_date = "na"
      return
    end_date_valid = util.ValidateDate(self.ride_end_date,
                                               'ride_end_date', problems)
    if end_date_valid == False:
      self.ride_end_date = "na"

  def validateGTFSfeedDate(self,problems):
    if util.IsEmpty(self.gtfs_feed_date):
      self.gtfs_feed_date = "na"
      return
    date_valid = util.ValidateDate(self.gtfs_feed_date,
                                               'gtfs_feed_date', problems)
    if date_valid == False:
      self.gtfs_feed_date = "na"

  def checkIfDatesValid(self,problems):
    if self.ride_start_date == "na" or self.ride_end_date == "na":
      self.validRideDates = 0
      problems.NoValidRideDatesRange('ride_start_date,ride_end_date')

  def checkFeedVersion(self,problems):
    if util.IsEmpty(self.ride_feed_version):
      return
    if self.ride_feed_version != self._schedule.feed_info.feed_version:
      problems.InvalidValue('ride_feed_version',self.ride_feed_version,'feed versions do no match')

    

  def Validate(self, problems=default_problem_reporter):
    """Validate attribute values and this object's internal consistency.

    Returns:
      True iff all validation checks passed.
    """
    found_problem = False
    found_problem = ((not util.ValidateRequiredFieldsAreNotEmpty(
                          self, self._REQUIRED_FIELD_NAMES, problems))
                          or found_problem)
    found_problem = self.validateCurrencyType(problems)
    found_problem = self.validateRideFiles(problems)
    found_problem = self.checkFeedVersion(problems)
    found_problem = self.validateGTFSfeedDate(problems)
    found_problem = self.validateRideDateRanges(problems)

    return not found_problem

  def ValidateBeforeAdd(self, problems):
    found_problem = self.validateRideStartdate(problems)
    found_problem = self.validateRideEnddate(problems)
    found_problem = self.checkIfDatesValid(problems)

    return True

  def ValidateAfterAdd(self, problems):
    self.Validate(problems)
    return

  def AddToSchedule(self, schedule, problems):
    schedule.AddRideTimes(self, problems,self.validRideDates)