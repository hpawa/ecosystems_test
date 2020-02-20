<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Groups</h1>
        <hr />
        <br />
        <br />
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" @click="initForm()" v-b-modal.user-modal>Add Group</button>
        <br />
        <br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>              
              <th scope="col">Role</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(group, index) in groups" :key="index">
              <td>{{ group.name }}</td>              
              <td>
                <button type="button" class="btn btn-warning btn-sm" @click="fillForm(user)" v-b-modal.user-modal>Update</button>
                <button type="button" class="btn btn-danger btn-sm" @click="onDeleteGroup(user)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="userModal" id="user-modal" :title="groupForm.title" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-username-group" label="Username:" label-for="form-username-input">
          <b-form-input
            id="form-username-input"
            type="text"
            v-model="groupForm.username"
            required
            placeholder="Enter username"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-password-group" label="Password:" label-for="form-password-input">
          <b-form-input
            id="form-password-input"
            type="password"
            v-model="groupForm.password"
            required
            placeholder="Enter password"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-group-group" label="Group:" label-for="form-group-select">
          <b-form-select
            id="form-group-select"
            v-model="groupForm.group"
            :options="groupsSelector"
            required
          ></b-form-select>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import Alert from './Alert.vue';
export default {
  components: {
    alert: Alert,
  },
  data() {
    return {
      message: '',
      showMessage: false,      
      groups: [],      
      groupForm: {
        groupID: null,
        name: "",
        title: "",
        method: ""
      }
    };
  },
  methods: {
    getGroups() {
      const path = "http://localhost:5000/groups";
      axios
        .get(path)
        .then(res => {
          this.groups = res.data.groups;
          this.getGroupsSelector();
        })
        .catch(error => {
          console.error(error);
        });
    },    
    addGroup(payload) {
      const path = "http://localhost:5000/groups";
      axios
        .post(path, payload)
        .then(res => {
          this.getGroups();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getGroups();
        });
    },
    removeGroup(groupID) {
      const path = `http://localhost:5000/groups/${groupID}`;
      axios
        .delete(path)
        .then(res => {
          this.getGroups();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getGroups();
        });
    },
    updateGroup(groupID, payload) {
      const path = `http://localhost:5000/users/${groupID}`;
      axios
        .put(path, payload)
        .then(res => {
          this.getGroups();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getGroups();
        });
    },
    onDeleteGroup(user){
      this.removeGroup(user.id);
    },
    initForm() {
      this.groupForm.name = "";
      this.groupForm.title = "Add Group"
      this.groupForm.method = "POST"
    },
    fillForm(group) {
      this.groupForm.username = user.username;
      this.groupForm.password = user.password;      
      this.groupForm.title = "Update Group";
      this.groupForm.method = "PUT";
      this.groupForm.groupID = group.id
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.userModal.hide();            
      const payload = {
        name: this.groupForm.username,
        password: this.groupForm.username,
        group_id: this.groupForm.group
      };
      if (this.groupForm.method == 'POST') {
        this.addUser(payload);
      }
      else if (this.groupForm.method == 'PUT') {        
        this.updateUser(this.groupForm.userID, payload)
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.userModal.hide();
      this.initForm();
    }
  },
  created() {    
    this.getGroups();    
  }
};
</script>