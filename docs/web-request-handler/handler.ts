class Handler {
    // private static API_ENDPOINT='https://habit-loop-python-rest-api.azurewebsites.net/habit/';
    private static API_ENDPOINT='https://gepardec-github-api.azurewebsites.net/view/gepardec/';

    public static async get(habit:string) : Promise<IHabitResponse> {
        console.log('hello')
        return new Promise<IHabitResponse> ((resolve,reject)=>{
            $.ajax(Handler.API_ENDPOINT+habit, {
                type: 'GET',
                dataType: 'json',
                error: (error)=>{
                    reject(error)
                },
                success: (success:IHabit[])=>{
                    resolve({
                        name: habit,
                        value: success.map((singleObject)=>({
                            ...singleObject,
                            viewDate: new Date( (singleObject.viewDate as unknown as number) * 1000)
                        }))
                    })
                },
            })
        })
    }
}