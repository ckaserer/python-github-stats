"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
class Handler {
    static get(habit) {
        return __awaiter(this, void 0, void 0, function* () {
            console.log('hello');
            return new Promise((resolve, reject) => {
                $.ajax(Handler.API_ENDPOINT + habit, {
                    type: 'GET',
                    dataType: 'json',
                    error: (error) => {
                        reject(error);
                    },
                    success: (success) => {
                        resolve({
                            name: habit,
                            value: success.map((singleObject) => (Object.assign(Object.assign({}, singleObject), { viewDate: new Date(singleObject.viewDate * 1000) })))
                        });
                    },
                });
            });
        });
    }
}
// private static API_ENDPOINT='https://habit-loop-python-rest-api.azurewebsites.net/habit/';
Handler.API_ENDPOINT = 'https://gepardec-github-api.azurewebsites.net/view/gepardec/';
