(function (window) {

    var clearBookmark = window.location.search.indexOf('clearbookmark=true') > -1,
        registration = window.rscpCfg.get("registrationToDeliver");

    // Check url parameter (passed on launch link) to determine whether to clear the 
    // bookmark or not
    if (clearBookmark) {

        // We'll go through the activities, and any that have a runtime.Location, we'll clear it
        registration.Activities.forEach((activity) => {
            if (activity.RunTime != null) {
                activity.RunTime.Location = null;

                // the location property may be where it stores the bookmark information,
                // but sometimes things like this are all stored in the suspend data. If that is the case,
                // you could also clear that with the following line. I'm leaving it commented because
                // suspend data may have more than just bookmarking, and you don't want to clear it 
                // out unless necessary. Even then, it may not be worth it if it affects the course's
                // 'memory' of other aspects of their journey.
                
                // activity.RunTime.SuspendData = null;
            }
        });

    }

    // *******************************************************
    // must call this last so the player continues loading
    rscpCustomizationCompleted();

})(window);