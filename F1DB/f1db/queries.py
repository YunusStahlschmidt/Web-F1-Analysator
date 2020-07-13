from F1DB.f1db import cursor
from F1DB.f1db.forms import drivers_dict

form_list = []


def race_and_results_queries():
    form = form_list[0]
    res_type = form.res_type.data
    season = form.season.data
    round = form.round.data
    driver = form.driver.data
    const = form.constructor.data
    fin_pos = form.fin_pos.data
    grid = form.grid.data
    fast_lap_rank = form.fast_lap_rank.data
    circuit = form.circuit.data
    status = form.status.data
    res_per = form.res_per.data
    page = form.page.data
    table = ""
    select_c = "select distinct "
    from_c = " from "
    join_c = ""
    where_c = ""

    if res_type == "CiI":
        table += "Circuit Table"
        select_c += "circuits.name, circuits.location, circuits.country, circuits.url "
        headings = ["Circuit", "City", "Country", "Info"]
        from_c += "circuits "
        join_races = "join races on circuits.circuitId = races.circuitId "
        is_races_joined = False
        join_results = "join results on races.raceId = results.raceId "
        is_results_joined = False
        join_drivers = "join drivers on results.driverId = drivers.driverId "
        join_constructors = "join constructors on results.constructorId = constructors.constructorId "
        join_status = "join status on results.statusId = status.statusId "
        if season != "All":
            join_c += join_races
            is_races_joined = True
            where_c += f"where races.year = {season} "
        if round != "All":
            where_c += f"and races.round = {round} "
        if driver != "All":
            driver_forename, driver_surname = drivers_dict[driver][0], drivers_dict[driver][1]
            if is_races_joined:
                join_c += join_results + join_drivers
                is_results_joined = True
                if where_c != "":
                    where_c += f"and drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
                else:
                    where_c += f"where drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
            else:
                join_c += join_races + join_results + join_drivers
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
                else:
                    where_c += f"where drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
        if const != "All":
            if is_races_joined:
                if is_results_joined:
                    join_c += join_constructors
                    if where_c != "":
                        where_c += f"and constructors.name = '{const}' "
                    else:
                        where_c += f"where constructors.name = '{const}' "
                else:
                    join_c += join_results + join_constructors
                    is_results_joined = True
                    if where_c != "":
                        where_c += f"and constructors.name = '{const}' "
                    else:
                        where_c += f"where constructors.name = '{const}' "
            else:
                join_c += join_races + join_results + join_constructors
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and constructors.name = '{const}' "
                else:
                    where_c += f"where constructors.name = '{const}' "
        if fin_pos != "All":
            if is_races_joined:
                if is_results_joined:
                    if where_c != "":
                        where_c += f"and results.positionText = '{fin_pos}' "
                    else:
                        where_c += f"where results.positionText = '{fin_pos}' "
                else:
                    join_c += join_results
                    is_results_joined = True
                    if where_c != "":
                        where_c += f"and results.positionText = '{fin_pos}' "
                    else:
                        where_c += f"where results.positionText = '{fin_pos}' "
            else:
                join_c += join_races + join_results
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.positionText = '{fin_pos}' "
                else:
                    where_c += f"where results.positionText = '{fin_pos}' "
        if grid != "All":
            if is_races_joined:
                if is_results_joined:
                    if where_c != "":
                        where_c += f"and results.grid = '{grid}' "
                    else:
                        where_c += f"where results.grid = '{grid}' "
                else:
                    join_c += join_results
                    is_results_joined = True
                    if where_c != "":
                        where_c += f"and results.grid = '{grid}' "
                    else:
                        where_c += f"where results.grid = '{grid}' "
            else:
                join_c += join_races + join_results
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.grid = '{grid}' "
                else:
                    where_c += f"where results.grid = '{grid}' "
        if fast_lap_rank != "All":
            if is_races_joined:
                if is_results_joined:
                    if where_c != "":
                        where_c += f"and results.rank = '{fast_lap_rank}' "
                    else:
                        where_c += f"where results.rank = '{fast_lap_rank}' "
                else:
                    join_c += join_results
                    is_results_joined = True
                    if where_c != "":
                        where_c += f"and results.rank = '{fast_lap_rank}' "
                    else:
                        where_c += f"where results.rank = '{fast_lap_rank}' "
            else:
                join_c += join_races + join_results
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.rank = '{fast_lap_rank}' "
                else:
                    where_c += f"where results.rank = '{fast_lap_rank}' "
        if circuit != "All":
            if where_c != "":
                where_c += f"and circuits.name = '{circuit}' "
            else:
                where_c += f"where circuits.name = '{circuit}' "
        if status != "All":
            if is_races_joined:
                if is_results_joined:
                    join_c += join_status
                    if where_c != "":
                        where_c += f"and status.status = '{status}' "
                    else:
                        where_c += f"where status.status = '{status}' "
                else:
                    join_c += join_results + join_status
                    is_results_joined = True
                    if where_c != "":
                        where_c += f"and status.status = '{status}' "
                    else:
                        where_c += f"where status.status = '{status}' "
            else:
                join_c += join_races + join_results + join_status
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and status.status = '{status}' "
                else:
                    where_c += f"where status.status = '{status}' "
        query = select_c + from_c + join_c + where_c
        cursor.execute(query)
        result = cursor.fetchall()
        return table, result, headings

    elif res_type == "CoI":
        table += "Constructor Table"
        select_c += "constructors.name, constructors.nationality, constructors.url "
        headings = ["Constructor", "Nationality", "Info"]
        from_c += "constructors "
        join_results = "join results on constructors.constructorId = results.constructorId "
        is_results_joined = False
        join_races = "join races on races.raceId = results.raceId "
        is_races_joined = False
        join_drivers = "join drivers on results.driverId = drivers.driverId "
        join_status = "join status on results.statusId = status.statusId "
        join_circuits = "join circuits on races.circuitId = circuits.circuitId "
        if season != "All":
            join_c += join_results + join_races
            is_results_joined = True
            is_races_joined = True
            where_c += f"where races.year = {season} "
        if round != "All":
            where_c += f"and races.round = {round} "
        if driver != "All":
            driver_forename, driver_surname = drivers_dict[driver][0], drivers_dict[driver][1]
            if is_results_joined:
                join_c += join_drivers
                if where_c != "":
                    where_c += f"and drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
                else:
                    where_c += f"where drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
            else:
                join_c += join_results + join_drivers
                is_results_joined = True
                if where_c != "":
                    where_c += f"and drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
                else:
                    where_c += f"where drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
        if const != "All":
            if where_c != "":
                where_c += f"and constructors.name = '{const}' "
            else:
                where_c += f"where constructors.name = '{const}' "
        if fin_pos != "All":
            if is_results_joined:
                if where_c != "":
                    where_c += f"and results.positionText = '{fin_pos}' "
                else:
                    where_c += f"where results.positionText = '{fin_pos}' "
            else:
                join_c += join_results
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.positionText = '{fin_pos}' "
                else:
                    where_c += f"where results.positionText = '{fin_pos}' "
        if grid != "All":
            if is_results_joined:
                if where_c != "":
                    where_c += f"and results.grid = '{grid}' "
                else:
                    where_c += f"where results.grid = '{grid}' "
            else:
                join_c += join_results
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.grid = '{grid}' "
                else:
                    where_c += f"where results.grid = '{grid}' "
        if fast_lap_rank != "All":
            if is_results_joined:
                if where_c != "":
                    where_c += f"and results.rank = '{fast_lap_rank}' "
                else:
                    where_c += f"where results.rank = '{fast_lap_rank}' "
            else:
                join_c += join_results
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.rank = '{fast_lap_rank}' "
                else:
                    where_c += f"where results.rank = '{fast_lap_rank}' "
        if circuit != "All":
            if is_results_joined:
                if is_races_joined:
                    join_c += join_circuits
                    if where_c != "":
                        where_c += f"and circuits.name = '{circuit}' "
                    else:
                        where_c += f"where circuits.name = '{circuit}' "
                else:
                    join_c += join_races + join_circuits
                    is_races_joined = True
                    if where_c != "":
                        where_c += f"and circuits.name = '{circuit}' "
                    else:
                        where_c += f"where circuits.name = '{circuit}' "
            else:
                join_c += join_results + join_races + join_circuits
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and circuits.name = '{circuit}' "
                else:
                    where_c += f"where circuits.name = '{circuit}' "
        if status != "All":
            if is_results_joined:
                join_c += join_status
                if where_c != "":
                    where_c += f"and status.status = '{status}' "
                else:
                    where_c += f"where status.status = '{status}' "
            else:
                join_c += join_results + join_status
                is_results_joined = True
                if where_c != "":
                    where_c += f"and status.status = '{status}' "
                else:
                    where_c += f"where status.status = '{status}' "
        query = select_c + from_c + join_c + where_c
        cursor.execute(query)
        result = cursor.fetchall()
        return table, result, headings

    elif res_type == "D":
        table += "Driver Table"
        select_c += "concat_ws(' ', drivers.forename, drivers.surname) as name, drivers.number, drivers.nationality, drivers.dob, drivers.url "
        headings = ["Name", "Starting Number", "Nationality", "DOB", "Info"]
        from_c += "drivers "
        join_results = "join results on drivers.driverId = results.driverId "
        is_results_joined = False
        join_races = "join races on races.raceId = results.raceId "
        is_races_joined = False
        join_constructors = "join constructors on results.constructorId = constructors.constructorId "
        join_status = "join status on results.statusId = status.statusId "
        join_circuits = "join circuits on races.circuitId = circuits.circuitId "
        if season != "All":
            join_c += join_results + join_races
            is_results_joined = True
            is_races_joined = True
            where_c += f"where races.year = {season} "
        if round != "All":
            where_c += f"and races.round = {round} "
        if driver != "All":
            driver_forename, driver_surname = drivers_dict[driver][0], drivers_dict[driver][1]
            if where_c != "":
                where_c += f"and drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
            else:
                where_c += f"where drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
        if const != "All":
            if is_results_joined:
                join_c += join_constructors
                if where_c != "":
                    where_c += f"and constructors.name = '{const}' "
                else:
                    where_c += f"where constructors.name = '{const}' "
            else:
                join_c += join_results + join_constructors
                is_results_joined = True
                if where_c != "":
                    where_c += f"and constructors.name = '{const}' "
                else:
                    where_c += f"where constructors.name = '{const}' "
        if fin_pos != "All":
            if is_results_joined:
                if where_c != "":
                    where_c += f"and results.positionText = '{fin_pos}' "
                else:
                    where_c += f"where results.positionText = '{fin_pos}' "
            else:
                join_c += join_results
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.positionText = '{fin_pos}' "
                else:
                    where_c += f"where results.positionText = '{fin_pos}' "
        if grid != "All":
            if is_results_joined:
                if where_c != "":
                    where_c += f"and results.grid = '{grid}' "
                else:
                    where_c += f"where results.grid = '{grid}' "
            else:
                join_c += join_results
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.grid = '{grid}' "
                else:
                    where_c += f"where results.grid = '{grid}' "
        if fast_lap_rank != "All":
            if is_results_joined:
                if where_c != "":
                    where_c += f"and results.rank = '{fast_lap_rank}' "
                else:
                    where_c += f"where results.rank = '{fast_lap_rank}' "
            else:
                join_c += join_results
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.rank = '{fast_lap_rank}' "
                else:
                    where_c += f"where results.rank = '{fast_lap_rank}' "
        if circuit != "All":
            if is_results_joined:
                if is_races_joined:
                    join_c += join_circuits
                    if where_c != "":
                        where_c += f"and circuits.name = '{circuit}' "
                    else:
                        where_c += f"where circuits.name = '{circuit}' "
                else:
                    join_c += join_races + join_circuits
                    is_races_joined = True
                    if where_c != "":
                        where_c += f"and circuits.name = '{circuit}' "
                    else:
                        where_c += f"where circuits.name = '{circuit}' "
            else:
                join_c += join_results + join_races + join_circuits
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and circuits.name = '{circuit}' "
                else:
                    where_c += f"where circuits.name = '{circuit}' "
        if status != "All":
            if is_results_joined:
                join_c += join_status
                if where_c != "":
                    where_c += f"and status.status = '{status}' "
                else:
                    where_c += f"where status.status = '{status}' "
            else:
                join_c += join_results + join_status
                is_results_joined = True
                if where_c != "":
                    where_c += f"and status.status = '{status}' "
                else:
                    where_c += f"where status.status = '{status}' "
        query = select_c + from_c + join_c + where_c
        cursor.execute(query)
        result = cursor.fetchall()
        return table, result, headings

    elif res_type == "QR":
        table += "Qualifying Table"
        select_c += "concat_ws(' ', races.year, races.name) as race, qualifying.position, concat_ws(' ', drivers.forename, drivers.surname) as name, constructors.name, qualifying.q1, qualifying.q2, qualifying.q3 "
        headings = ["Race", "Pos", "Driver", "Constructor", "Q1", "Q2", "Q3"]
        from_c += "qualifying "
        join_results = "join results on drivers.driverId = results.driverId "
        is_results_joined = False
        join_races = "join races on races.raceId = qualifying.raceId "
        is_races_joined = False
        join_constructors = "join constructors on qualifying.constructorId = constructors.constructorId "
        join_status = "join status on results.statusId = status.statusId "
        join_circuits = "join circuits on races.circuitId = circuits.circuitId "
        join_drivers = "join drivers on qualifying.driverId = drivers.driverId "
        join_c += join_drivers + join_constructors + join_races
        if season != "All":
            where_c += f"where races.year = {season} "
        if round != "All":
            where_c += f"and races.round = {round} "
        if driver != "All":
            driver_forename, driver_surname = drivers_dict[driver][0], drivers_dict[driver][1]
            if where_c != "":
                where_c += f"and drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
            else:
                where_c += f"where drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
        if const != "All":
            if where_c != "":
                where_c += f"and constructors.name = '{const}' "
            else:
                where_c += f"where constructors.name = '{const}' "
        if fin_pos != "All":
            join_c += join_results
            is_results_joined = True
            if where_c != "":
                where_c += f"and results.positionText = '{fin_pos}' "
            else:
                where_c += f"where results.positionText = '{fin_pos}' "
        if grid != "All":
            if is_results_joined:
                if where_c != "":
                    where_c += f"and results.grid = '{grid}' "
                else:
                    where_c += f"where results.grid = '{grid}' "
            else:
                join_c += join_results
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.grid = '{grid}' "
                else:
                    where_c += f"where results.grid = '{grid}' "
        if fast_lap_rank != "All":
            if is_results_joined:
                if where_c != "":
                    where_c += f"and results.rank = '{fast_lap_rank}' "
                else:
                    where_c += f"where results.rank = '{fast_lap_rank}' "
            else:
                join_c += join_results
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.rank = '{fast_lap_rank}' "
                else:
                    where_c += f"where results.rank = '{fast_lap_rank}' "
        if circuit != "All":
            join_c += join_circuits
            if where_c != "":
                where_c += f"and circuits.name = '{circuit}' "
            else:
                where_c += f"where circuits.name = '{circuit}' "
        if status != "All":
            if is_results_joined:
                join_c += join_status
                if where_c != "":
                    where_c += f"and status.status = '{status}' "
                else:
                    where_c += f"where status.status = '{status}' "
            else:
                join_c += join_results + join_status
                is_results_joined = True
                if where_c != "":
                    where_c += f"and status.status = '{status}' "
                else:
                    where_c += f"where status.status = '{status}' "
        query = select_c + from_c + join_c + where_c + " order by races.year, races.round, qualifying.position "
        cursor.execute(query)
        result = cursor.fetchall()
        return table, result, headings

    elif res_type == "RR":
        table += "Results Table"
        select_c += "concat_ws(' ', races.year, races.name) as race, results.positionText, concat_ws(' ', drivers.forename, drivers.surname) as name," \
                    " constructors.name, results.laps, results.grid, results.time, status.status, results.points "
        headings = ["Race", "Pos", "Driver", "Constructor", "Laps", "Grid", "Time", "Status", "Points"]
        from_c += "results "
        join_races = "join races on races.raceId = results.raceId "
        join_constructors = "join constructors on results.constructorId = constructors.constructorId "
        join_status = "join status on results.statusId = status.statusId "
        join_drivers = "join drivers on results.driverId = drivers.driverId "
        join_circuits = "join circuits on races.circuitId = circuits.circuitId "
        join_c += join_drivers + join_constructors + join_races + join_status
        if season != "All":
            where_c += f"where races.year = {season} "
        if round != "All":
            where_c += f"and races.round = {round} "
        if driver != "All":
            driver_forename, driver_surname = drivers_dict[driver][0], drivers_dict[driver][1]
            if where_c != "":
                where_c += f"and drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
            else:
                where_c += f"where drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
        if const != "All":
            if where_c != "":
                where_c += f"and constructors.name = '{const}' "
            else:
                where_c += f"where constructors.name = '{const}' "
        if fin_pos != "All":

            if where_c != "":
                where_c += f"and results.positionText = '{fin_pos}' "
            else:
                where_c += f"where results.positionText = '{fin_pos}' "
        if grid != "All":
            if where_c != "":
                where_c += f"and results.grid = '{grid}' "
            else:
                where_c += f"where results.grid = '{grid}' "
        if fast_lap_rank != "All":
            if where_c != "":
                where_c += f"and results.rank = '{fast_lap_rank}' "
            else:
                where_c += f"where results.rank = '{fast_lap_rank}' "
        if circuit != "All":
            join_c += join_circuits
            if where_c != "":
                where_c += f"and circuits.name = '{circuit}' "
            else:
                where_c += f"where circuits.name = '{circuit}' "
        if status != "All":
            if where_c != "":
                where_c += f"and status.status = '{status}' "
            else:
                where_c += f"where status.status = '{status}' "
        query = select_c + from_c + join_c + where_c + " order by races.year, races.round, results.positionOrder "
        cursor.execute(query)
        result = cursor.fetchall()
        return table, result, headings

    elif res_type == "RS":
        table += "Race Table"
        select_c += "races.year, races.round, races.name, races.date, circuits.name, circuits.location, circuits.country, races.url "
        headings = ["Season", "Round", "Name", "Date", "Circuit", "City", "Country", "Info"]
        from_c += "races "
        join_c += "join circuits on races.circuitId = circuits.circuitId "
        join_results = "join results on races.raceId = results.raceId "
        is_results_joined = False
        join_constructors = "join constructors on results.constructorId = constructors.constructorId "
        join_drivers = "join drivers on results.driverId = drivers.driverId "
        join_status = "join status on results.statusId = status.statusId "
        order = ""
        if season != "All":
            where_c += f"where races.year = {season} "
        else:
            order += " order by races.year, races.round "
        if round != "All":
            where_c += f"and races.round = {round} "
        if driver != "All":
            driver_forename, driver_surname = drivers_dict[driver][0], drivers_dict[driver][1]
            if is_results_joined:
                join_c += join_drivers
                if where_c != "":
                    where_c += f"and drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
                else:
                    where_c += f"where drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
            else:
                join_c += join_results + join_drivers
                is_results_joined = True
                if where_c != "":
                    where_c += f"and drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
                else:
                    where_c += f"where drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
        if const != "All":
            if is_results_joined:
                join_c += join_constructors
                if where_c != "":
                    where_c += f"and constructors.name = '{const}' "
                else:
                    where_c += f"where constructors.name = '{const}' "
            else:
                join_c += join_results + join_constructors
                is_results_joined = True
                if where_c != "":
                    where_c += f"and constructors.name = '{const}' "
                else:
                    where_c += f"where constructors.name = '{const}' "
        if fin_pos != "All":
            if is_results_joined:
                if where_c != "":
                    where_c += f"and results.positionText = '{fin_pos}' "
                else:
                    where_c += f"where results.positionText = '{fin_pos}' "
            else:
                join_c += join_results
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.positionText = '{fin_pos}' "
                else:
                    where_c += f"where results.positionText = '{fin_pos}' "
        if grid != "All":
            if is_results_joined:
                if where_c != "":
                    where_c += f"and results.grid = '{grid}' "
                else:
                    where_c += f"where results.grid = '{grid}' "
            else:
                join_c += join_results
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.grid = '{grid}' "
                else:
                    where_c += f"where results.grid = '{grid}' "
        if fast_lap_rank != "All":
            if is_results_joined:
                if where_c != "":
                    where_c += f"and results.rank = '{fast_lap_rank}' "
                else:
                    where_c += f"where results.rank = '{fast_lap_rank}' "
            else:
                join_c += join_results
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.rank = '{fast_lap_rank}' "
                else:
                    where_c += f"where results.rank = '{fast_lap_rank}' "
        if circuit != "All":
            if where_c != "":
                where_c += f"and circuits.name = '{circuit}' "
            else:
                where_c += f"where circuits.name = '{circuit}' "
        if status != "All":
            if is_results_joined:
                join_c += join_status
                if where_c != "":
                    where_c += f"and status.status = '{status}' "
                else:
                    where_c += f"where status.status = '{status}' "
            else:
                join_c += join_results + join_status
                is_results_joined = True
                if where_c != "":
                    where_c += f"and status.status = '{status}' "
                else:
                    where_c += f"where status.status = '{status}' "
        if order == "":
            order += " order by races.round "
        query = select_c + from_c + join_c + where_c + order
        cursor.execute(query)
        result = cursor.fetchall()
        return table, result, headings

    elif res_type == "SL":
        table += "Season Table"
        select_c += "seasons.year, seasons.url "
        headings = ["Year", "Info"]
        from_c += "seasons "
        join_races = "join races on seasons.year = races.year "
        is_races_joined = False
        join_results = "join results on races.raceId = results.raceId "
        is_results_joined = False
        join_drivers = "join drivers on results.driverId = drivers.driverId "
        join_constructors = "join constructors on results.constructorId = constructors.constructorId "
        join_circuits = "join circuits on races.circuitId = circuits.circuitId "
        join_status = "join status on results.statusId = status.statusId "
        order = ""
        if season != "All":
            where_c += f"where seasons.year = {season} "
        if round != "All":
            join_c += join_races
            where_c += f"and races.round = {round} "
        if driver != "All":
            driver_forename, driver_surname = drivers_dict[driver][0], drivers_dict[driver][1]
            if is_races_joined:
                join_c += join_results + join_drivers
                is_results_joined = True
                if where_c != "":
                    where_c += f"and drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
                else:
                    where_c += f"where drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
            else:
                join_c += join_races + join_results + join_drivers
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
                else:
                    where_c += f"where drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
        if const != "All":
            if is_races_joined:
                if is_results_joined:
                    join_c += join_constructors
                    if where_c != "":
                        where_c += f"and constructors.name = '{const}' "
                    else:
                        where_c += f"where constructors.name = '{const}' "
                else:
                    join_c += join_results + join_constructors
                    is_results_joined = True
                    if where_c != "":
                        where_c += f"and constructors.name = '{const}' "
                    else:
                        where_c += f"where constructors.name = '{const}' "
            else:
                join_c += join_races + join_results + join_constructors
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and constructors.name = '{const}' "
                else:
                    where_c += f"where constructors.name = '{const}' "
        if fin_pos != "All":
            if is_races_joined:
                if is_results_joined:
                    if where_c != "":
                        where_c += f"and results.positionText = '{fin_pos}' "
                    else:
                        where_c += f"where results.positionText = '{fin_pos}' "
                else:
                    join_c += join_results
                    is_results_joined = True
                    if where_c != "":
                        where_c += f"and results.positionText = '{fin_pos}' "
                    else:
                        where_c += f"where results.positionText = '{fin_pos}' "
            else:
                join_c += join_races + join_results
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.positionText = '{fin_pos}' "
                else:
                    where_c += f"where results.positionText = '{fin_pos}' "
        if grid != "All":
            if is_races_joined:
                if is_results_joined:
                    if where_c != "":
                        where_c += f"and results.grid = '{grid}' "
                    else:
                        where_c += f"where results.grid = '{grid}' "
                else:
                    join_c += join_results
                    is_results_joined = True
                    if where_c != "":
                        where_c += f"and results.grid = '{grid}' "
                    else:
                        where_c += f"where results.grid = '{grid}' "
            else:
                join_c += join_races + join_results
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.grid = '{grid}' "
                else:
                    where_c += f"where results.grid = '{grid}' "
        if fast_lap_rank != "All":
            if is_races_joined:
                if is_results_joined:
                    if where_c != "":
                        where_c += f"and results.rank = '{fast_lap_rank}' "
                    else:
                        where_c += f"where results.rank = '{fast_lap_rank}' "
                else:
                    join_c += join_results
                    is_results_joined = True
                    if where_c != "":
                        where_c += f"and results.rank = '{fast_lap_rank}' "
                    else:
                        where_c += f"where results.rank = '{fast_lap_rank}' "
            else:
                join_c += join_races + join_results
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and results.rank = '{fast_lap_rank}' "
                else:
                    where_c += f"where results.rank = '{fast_lap_rank}' "
        if circuit != "All":
            if is_races_joined:
                join_c += join_circuits
                if where_c != "":
                    where_c += f"and circuits.name = '{circuit}' "
                else:
                    where_c += f"where circuits.name = '{circuit}' "
            else:
                join_c += join_races + join_circuits
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and circuits.name = '{circuit}' "
                else:
                    where_c += f"where circuits.name = '{circuit}' "
        if status != "All":
            if is_races_joined:
                if is_results_joined:
                    join_c += join_status
                    if where_c != "":
                        where_c += f"and status.status = '{status}' "
                    else:
                        where_c += f"where status.status = '{status}' "
                else:
                    join_c += join_results + join_status
                    is_results_joined = True
                    if where_c != "":
                        where_c += f"and status.status = '{status}' "
                    else:
                        where_c += f"where status.status = '{status}' "
            else:
                join_c += join_races + join_results + join_status
                is_races_joined = True
                is_results_joined = True
                if where_c != "":
                    where_c += f"and status.status = '{status}' "
                else:
                    where_c += f"where status.status = '{status}' "
        if order == "":
            order += " order by seasons.year "
        query = select_c + from_c + join_c + where_c + order
        cursor.execute(query)
        result = cursor.fetchall()
        return table, result, headings

    elif res_type == "FS":
        table += "Status Table"
        select_c += "status.status, count(results.statusId) as count "
        headings = ["Status", "Count"]
        from_c += "results "
        join_c += "join status on results.statusId = status.statusId "
        join_races = "join races on results.raceId = races.raceId "
        is_races_joined = False
        join_constructors = "join constructors on results.constructorId = constructors.constructorId "
        join_drivers = "join drivers on results.driverId = drivers.driverId "
        join_circuits = "join circuits on races.circuitId = circuits.circuitId "
        order = ""
        if season != "All":
            join_c += join_races
            is_races_joined = True
            where_c += f"where races.year = {season} "
        if round != "All":
            where_c += f"and races.round = {round} "
        if driver != "All":
            driver_forename, driver_surname = drivers_dict[driver][0], drivers_dict[driver][1]
            join_c += join_drivers
            if where_c != "":
                where_c += f"and drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
            else:
                where_c += f"where drivers.forename = '{driver_forename}' and drivers.surname = '{driver_surname}' "
        if const != "All":
            join_c += join_constructors
            if where_c != "":
                where_c += f"and constructors.name = '{const}' "
            else:
                where_c += f"where constructors.name = '{const}' "
        if fin_pos != "All":
            if where_c != "":
                where_c += f"and results.positionText = '{fin_pos}' "
            else:
                where_c += f"where results.positionText = '{fin_pos}' "
        if grid != "All":
            if where_c != "":
                where_c += f"and results.grid = '{grid}' "
            else:
                where_c += f"where results.grid = '{grid}' "
        if fast_lap_rank != "All":
            if where_c != "":
                where_c += f"and results.rank = '{fast_lap_rank}' "
            else:
                where_c += f"where results.rank = '{fast_lap_rank}' "
        if circuit != "All":
            if is_races_joined:
                join_c += join_circuits
                if where_c != "":
                    where_c += f"and circuits.name = '{circuit}' "
                else:
                    where_c += f"where circuits.name = '{circuit}' "
            else:
                join_c += join_races + join_circuits
                is_races_joined = True
                if where_c != "":
                    where_c += f"and circuits.name = '{circuit}' "
                else:
                    where_c += f"where circuits.name = '{circuit}' "
        if status != "All":
            if where_c != "":
                where_c += f"and status.status = '{status}' "
            else:
                where_c += f"where status.status = '{status}' "
        if order == "":
            order += " order by status.statusId "
        query = select_c + from_c + join_c + where_c + " group by status.status " + order
        cursor.execute(query)
        result = cursor.fetchall()
        return table, result, headings


