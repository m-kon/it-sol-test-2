let CompanyComponent = {
    props: ['company'],
    template: '<li class="list-group-item"><div class="col-sm-4">{{company.company_id}}</div><div class="col-sm-4">{{company.title}}</div><div class="col-sm-4">{{company.date_create}}</div></li>'
}

vm = new Vue({
    el: '#front',
    data: {
	companies: [],
	is_there_companies: false
    },
    components: {
	'company-component': CompanyComponent
    },
    methods: {
	getDoublesList: function() {
	    console.log('get doubles start');
	    this.$http.get('get_bitrix')
		.then((res) => {
		    //console.log(res.data);
		    let companies = res.data;
		    //console.log('companies: ' + companies);
		    //console.log('res.data: ' + res.data);
		    //if (companies == res.data) { console.log(1) }
		    //console.log(companies.lenght);
		    //if (companies != undefined) {
		    for (i in companies) {
			let rec = { 'company_id': null, 'title': null, 'date_create': null };
			rec.company_id = companies[i]['ID'];
			rec.title = companies[i]['TITLE'];
			rec.date_create = companies[i]['DATE_CREATE'];
			this.companies.push(rec)
		    }
		    this.is_there_companies = true
		})
	}
    }
})
