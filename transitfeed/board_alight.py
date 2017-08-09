# Copyright (C) 2017 Oregon Department of Transportation (ODOT)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from problems import default_problem_reporter
from gtfsobjectbase import GtfsObjectBase
import util
from loader import Loader
import gtfsfactory as gtfsfactory_module


class Board_alight(GtfsObjectBase):
  """This class represents a rule that determines which itineraries a
  fare rule applies to."""
  _REQUIRED_FIELD_NAMES = ['trip_id','stop_id','stop_sequence','record_use']
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + [
                                         'schedule_relationship',
                                         'boardings',
                                         'alightings',
                                         'current_load',
                                         'load_type',
                                         'rack_down',
                                         'bike_boardings',
                                         'bike_alightings',
                                         'ramp_used',
                                         'ramp_boardings',
                                         'ramp_alightings',
                                         'service_date',
                                         'service_arrival_time',
                                         'service_departure_time',
                                         'source'
                                         ]
  _TABLE_NAME = "board_alight"

  trips = None

  def __init__(self,trip_id = None,stop_id = None,stop_sequence = None,record_use = None, 
              schedule_relationship = None,boardings=None,alightings=None,current_load=None,load_type=None,rack_down = None,
              bike_boardings=None,bike_alightings=None,ramp_used = None,ramp_boardings=None,ramp_alightings=None,
              service_date = None,service_arrival_time = None,service_departure_time = None,source=None,field_dict=None,**kwargs):
    
    
    self._schedule = None

    if not field_dict:
      if trip_id:
        kwargs['trip_id'] = trip_id
      if stop_id:
        kwargs['stop_id'] = stop_id
      if stop_sequence:
        kwargs['stop_sequence'] = stop_sequence
      if record_use:
        kwargs['record_use'] = record_use
      if schedule_relationship:
        kwargs['schedule_relationship'] = schedule_relationship
      if boardings:
        kwargs['boardings'] = boardings
      if alightings:
        kwargs['alightings'] = alightings
      if bike_boardings:
        kwargs['bike_boardings'] = bike_boardings
      if bike_alightings:
        kwargs['bike_alightings'] = bike_alightings
      if ramp_boardings:
        kwargs['ramp_boardings'] = ramp_boardings
      if ramp_alightings:
        kwargs['ramp_alightings'] = ramp_alightings
      if load_type:
        kwargs['load_type'] = load_type
      if current_load:
        kwargs['current_load'] = current_load
      if rack_down:
        kwargs['rack_down'] = rack_down
      if ramp_used:
        kwargs['ramp_used'] = ramp_used
      if service_arrival_time:
        kwargs['service_arrival_time'] = service_arrival_time
      if service_departure_time:
        kwargs['service_departure_time'] = service_departure_time
      if service_date:
        kwargs['service_date'] = service_date
      if source:
        kwargs['source'] = source
      field_dict = kwargs
    self.__dict__.update(field_dict)

      

  def ValidateBoardingsHasValidValue(self, problems):
    if util.IsEmpty(self.boardings):
        self.boardings = 0
        return
    try:
      self.boardings = int(self.boardings)
    except (ValueError, TypeError):
      problems.InvalidValue('boardings', self.boardings,
          'Value must be non negative integer')
      del self.boardings
      return
    if self.boardings < 0:
      problems.InvalidValue('boardings', self.boardings,
          'Value must be non negative integer')
    

  def ValidateAlightingsHasValidValue(self, problems):
    if util.IsEmpty(self.alightings):
        self.alightings = 0
        return
    try:
      self.alightings = int(self.alightings)
    except (ValueError, TypeError):
      problems.InvalidValue('alightings', self.alightings,
          'Value must be non negative integer')
      del self.alightings
      return
    if self.alightings < 0:
      problems.InvalidValue('alightings', self.alightings,
          'Value must be non negative integer')
    

  def ValidateBikeBoardingsHasValidValue(self, problems):
    if util.IsEmpty(self.bike_boardings):
        self.bike_boardings = 0
        return
    try:
      self.bike_boardings = int(self.bike_boardings)
    except (ValueError, TypeError):
      problems.InvalidValue('bike_boardings', self.bike_boardings,
          'Value must be non negative integer')
      del self.bike_boardings
      return
    if self.bike_boardings < 0:
      problems.InvalidValue('bike_boardings', self.bike_boardings,
          'Value must be non negative integer')

  def ValidateBikeAlightingsHasValidValue(self, problems):
    if util.IsEmpty(self.bike_alightings):
        self.bike_alightings = 0
        return
    try:
      self.bike_alightings = int(self.bike_alightings)
    except (ValueError, TypeError):
      problems.InvalidValue('bike_alightings', self.bike_alightings,
          'Value must be non negative integer')
      del self.bike_alightings
      return
    if self.bike_alightings < 0:
      problems.InvalidValue('bike_alightings', self.bike_alightings,
          'Value must be non negative integer')
  
  def ValidateRampBoardingsHasValidValue(self, problems):
    if util.IsEmpty(self.ramp_boardings):
        self.ramp_boardings = 0
        return
    try:
      self.ramp_boardings = int(self.ramp_boardings)
    except (ValueError, TypeError):
      problems.InvalidValue('ramp_boardings', self.ramp_boardings,
          'Value must be non negative integer')
      del self.ramp_boardings
      return
    if self.ramp_boardings < 0:
      problems.InvalidValue('ramp_boardings', self.ramp_boardings,
          'Value must be non negative integer')

  def ValidateRampAlightingsHasValidValue(self, problems):
    if util.IsEmpty(self.ramp_alightings):
        self.ramp_alightings = 0
        return
    try:
      self.ramp_alightings = int(self.ramp_alightings)
    except (ValueError, TypeError):
      problems.InvalidValue('ramp_alightings', self.ramp_alightings,
          'Value must be non negative integer')
      del self.ramp_alightings
      return
    if self.ramp_alightings < 0:
      problems.InvalidValue('ramp_alightings', self.ramp_alightings,
          'Value must be non negative integer')

  def validateSource(self,problems):
    if self.source is not None:
      if util.IsEmpty(self.source):
        self.source = 0
        return
      try:
        self.source = int(self.source)
      except (ValueError, TypeError):
        problems.InvalidValue('source', self.source)
        del self.source
        return
      if self.source not in (0,1,2,3,4):
        problems.InvalidValue('source', self.source,
            'Should be 0,1,2,3 or 4')

  def validateCurrentLoad(self,problems):
    if util.IsEmpty(self.current_load):
      self.current_load = 0
      return
    try:
      self.current_load = int(self.current_load)
    except (ValueError, TypeError):
      problems.InvalidValue('current_load', self.current_load)
      del self.current_load
      return
    if self.current_load < 0 or self.current_load > 100:
      problems.InvalidValue('current_load', self.current_load,
          'Must be between 0 and 100')

  def validateServiceArrivalTimeFormat(self,problems):
    if util.IsEmpty(self.service_arrival_time):
      self.service_arrival_time = 0
      return
    accept = util.checkInProperTimeFormat(self.service_arrival_time)
    if accept == 0:
      problems.UnknownTimeFormat('service_arrival_time',self.service_arrival_time)


  def validateServiceDepartureTimeFormat(self,problems):
    if util.IsEmpty(self.service_departure_time):
      self.service_departure_time = 0
      return
    accept = util.checkInProperTimeFormat(self.service_departure_time)
    if accept == 0:
      problems.UnknownTimeFormat('service_departure_time',self.service_departure_time)

  def validateServiceDate(self,problems):
    if util.IsEmpty(self.service_date):
      return
    valid_date = util.ValidateDate(self.service_date,
                                               'service_date', problems)
    if self._schedule.validRideDates == 0:
      return
    if valid_date:
      if self.service_date > self._schedule.ride_feed_date[1] or self.service_date < self._schedule.ride_feed_date[0]:
        problems.InvalidValue('service_date',self.service_date,'Service date does not fall in valid range')

  def validateLoadType(self,problems):
    if util.IsEmpty(self.load_type):
      self.load_type = 0
      return
    try:
      self.load_type = int(self.load_type)
    except (ValueError, TypeError):
      problems.InvalidValue('load_type', self.load_type)
      del self.load_type
      return
    if self.load_type not in (0, 1):
      problems.InvalidValue('load_type', self.load_type,
          'Must be 0 or 1')

  def validateRecordUse(self,problems):
    if util.IsEmpty(self.record_use):
        self.record_use = 0
        return
    try:
      self.record_use = int(self.record_use)
    except (ValueError, TypeError):
      problems.InvalidValue('record_use', self.record_use,
          'Value must be 0 or 1')
      del self.record_use
      return
    if self.record_use not in (0, 1):
      problems.InvalidValue('record_use', self.record_use,
          'Value must be 0 or 1')

  def validateRackDown(self,problems):
    if util.IsEmpty(self.rack_down):
        self.rack_down = 0
        return
    try:
      self.rack_down = int(self.rack_down)
    except (ValueError, TypeError):
      problems.InvalidValue('rack_down', self.rack_down,
          'Value must be 0 or 1')
      del self.rack_down
      return
    if self.rack_down not in (0, 1):
      problems.InvalidValue('rack_down', self.rack_down,
          'Value must be 0 or 1')

  def validateRampUsed(self,problems):
    if util.IsEmpty(self.ramp_used):
        self.ramp_used = 0
        return
    try:
      self.ramp_used = int(self.ramp_used)
    except (ValueError, TypeError):
      problems.InvalidValue('ramp_used', self.ramp_used,
          'Value must be 0 or 1')
      del self.ramp_used
      return
    if self.ramp_used not in (0, 1):
      problems.InvalidValue('ramp_used', self.ramp_used,
          'Value must be 0 or 1')

  def validateScheduleRelationship(self,problems):
    if util.IsEmpty(self.schedule_relationship):
        self.schedule_relationship = 0
        return
    try:
      self.schedule_relationship = int(self.schedule_relationship)
    except (ValueError, TypeError):
      problems.InvalidValue('schedule_relationship', self.schedule_relationship,
          'Value must be in range 0 to 8')
      del self.schedule_relationship
      return
    if self.schedule_relationship < 0 or self.schedule_relationship > 8:
      problems.InvalidValue('schedule_relationship', self.schedule_relationship,
          'Value must be in range 0 to 8')

  def validateStopSequence(self,problems):
    if self.stop_sequence not in self._schedule.stop_sequences:
      problems.InvalidValue('stop_sequence',self.stop_sequence,'Did not find a matching stop_sequence in stop_times.txt')

  def validateTripId(self,problems):
    if self.trip_id not in self._schedule.trips.keys():
      problems.InvalidValue('trip_id',self.trip_id,'Did not find a matching trip_id in trips.txt')

  def validateStopId(self,problems):
    if self.stop_id not in self._schedule.stops.keys():
      problems.InvalidValue('stop_id',self.stop_id,'Did not find a matching stop_id in stops.txt')

  def Validate(self, problems=default_problem_reporter):
    """Validate attribute values and this object's internal consistency.

    Returns:
      True iff all validation checks passed.
    """
    found_problem = False
    found_problem = ((not util.ValidateRequiredFieldsAreNotEmpty(
                          self, self._REQUIRED_FIELD_NAMES, problems))
                          or found_problem)
    found_problem = self.ValidateBoardingsHasValidValue(problems)
    found_problem = self.ValidateAlightingsHasValidValue(problems)
    found_problem = self.ValidateBikeBoardingsHasValidValue(problems)
    found_problem = self.ValidateBikeAlightingsHasValidValue(problems)
    found_problem = self.ValidateRampBoardingsHasValidValue(problems)
    found_problem = self.ValidateRampAlightingsHasValidValue(problems)
    found_problem = self.validateSource(problems)
    found_problem = self.validateCurrentLoad(problems)
    found_problem = self.validateServiceArrivalTimeFormat(problems)
    found_problem = self.validateServiceDepartureTimeFormat(problems)
    found_problem = self.validateLoadType(problems)
    found_problem = self.validateRecordUse(problems)
    found_problem = self.validateRampUsed(problems)
    found_problem = self.validateRackDown(problems)
    found_problem = self.validateScheduleRelationship(problems)
    found_problem = self.validateStopSequence(problems)
    found_problem = self.validateTripId(problems)
    found_problem = self.validateStopId(problems)
    found_problem = self.validateServiceDate(problems)
    
    return not found_problem

  def ValidateBeforeAdd(self, problems):
    return True

  def ValidateAfterAdd(self, problems):
    self.Validate(problems)

  def AddToSchedule(self, schedule, problems):
    schedule.AddBoardAlightObject(self, problems)

  