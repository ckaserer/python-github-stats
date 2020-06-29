"use strict";
class ChartHelper {
    static transformData(response, minDate, maxDate) {
        let returnValue = [];
        for (let newDate = new Date(minDate); newDate <= maxDate; newDate.setDate(newDate.getDate() + 1)) {
            returnValue.push({
                date: new Date(newDate),
                count: NaN,
                habits: []
            });
        }
        response.value.forEach((habit) => {
            const day = habit.viewDate.getDate(), month = habit.viewDate.getMonth(), year = habit.viewDate.getFullYear();
            let values = returnValue.filter((value) => {
                return day == value.date.getDate() && month == value.date.getMonth() && year == value.date.getFullYear();
            });
            if (values.length != 0) {
                values[0].habits.push(habit);
                values[0].count = habit.uniques;
            }
        });
        returnValue = returnValue.sort((value1, value2) => {
            return value1.date.getTime() - value2.date.getTime();
        });
        // let myCounter=0
        // returnValue.forEach(element => {
        //     myCounter+= element.habits.length
        //     if ( element.habits.length == 0) {
        //         myCounter = 0
        //     }
        //     element.count = myCounter
        // });
        return returnValue;
    }
}
