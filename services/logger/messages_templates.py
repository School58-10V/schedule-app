from services.messages_manager import MessagesManager


class MessagesTemplates:
    messages_manager = MessagesManager()

    @classmethod
    def get_messages_manager(cls):
        return cls.messages_manager

    class General:

        @classmethod
        def get_id_not_found_message(cls, model, object_id):
            return MessagesTemplates.messages_manager.get_message("general.id_not_found", {"model": model, "object_id": object_id})
        
        @classmethod
        def get_validation_error_message(cls, err):
            return MessagesTemplates.messages_manager.get_message("general.validation_error", {"err": err})
        
        @classmethod
        def get_object_id_mismatch_message(cls):
            return MessagesTemplates.messages_manager.get_message("general.validation_error")
        
        @classmethod
        def get_missing_fields_message(cls, fields):
            return MessagesTemplates.messages_manager.get_message("general.missing_fields", {"fields": fields})
        
        @classmethod
        def get_malformed_input_message(cls):
            return MessagesTemplates.messages_manager.get_message("general.malformed_input")
    
    class Adapter:
        pass
    
    class Authentication:

        @classmethod
        def get_login_attempt_message(cls):
            return MessagesTemplates.messages_manager.get_message("authentication.login_attempt")
        
        @classmethod
        def get_wrong_login_message(cls, login):
            return MessagesTemplates.messages_manager.get_message("authentication.wrong_login", {"login": login})
        
        @classmethod
        def get_wrong_password_message(cls):
            return MessagesTemplates.messages_manager.get_message("authentication.wrong_password")
        
        @classmethod
        def get_login_success_message(cls):
            return MessagesTemplates.messages_manager.get_message("authentication.login_success")
        
        @classmethod
        def get_register_attempt_message(cls):
            return MessagesTemplates.messages_manager.get_message("authentication.register_attempt")
        
        @classmethod
        def get_register_success_message(cls):
            return MessagesTemplates.messages_manager.get_message("authentication.register_success")
        
        @classmethod
        def get_on_request_message(cls, method, path, host, host_url):
            return MessagesTemplates.messages_manager.get_message("authentication.on_request", {"method": method, "path": path, "host": host, "host_url": host_url})
        
        @classmethod
        def get_malformed_request_message(cls):
            return MessagesTemplates.messages_manager.get_message("authentication.malformed_request")
        
        @classmethod
        def get_token_not_found_message(cls):
            return MessagesTemplates.messages_manager.get_message("authentication.token_not_found")
        
        @classmethod
        def get_session_change_message(cls):
            return MessagesTemplates.messages_manager.get_message("authentication.session_change")

    class Controller:

        class Success:

            @classmethod
            def get_collect_all_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.success.collect_all", {"model": model})
            
            @classmethod
            def get_collect_all_detailed_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.success.collect_all_detailed", {"model": model})
            
            @classmethod
            def get_collect_all_by_model_message(cls, model, filter):
                return MessagesTemplates.messages_manager.get_message("controller.success.collect_all_by_model", {"model": model, "filter": filter})
            
            @classmethod
            def get_find_by_id_message(cls, model, object_id):
                return MessagesTemplates.messages_manager.get_message("controller.success.find_by_id", {"model": model, "object_id": object_id})
            
            @classmethod
            def get_find_by_id_detailed_message(cls, model, object_id):
                return MessagesTemplates.messages_manager.get_message("controller.success.find_by_id_detailed", {"model": model, "object_id": object_id})
            
            @classmethod
            def get_find_by_day_and_student_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.success.find_by_day_and_student", {"model": model})
            
            @classmethod
            def get_find_current_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.success.find_current", {"model": model})
            
            @classmethod
            def get_create_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.success.create", {"model": model})
            
            @classmethod
            def get_update_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.success.update", {"model": model})
            
            @classmethod
            def get_delete_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.success.delete", {"model": model})

            @classmethod
            def get_upload_files_message(cls):
                return MessagesTemplates.messages_manager.get_message("controller.success.upload_files")
            
            @classmethod
            def get_save_timetable_message(cls):
                return MessagesTemplates.messages_manager.get_message("controller.success.save_timetable")
            
            @classmethod
            def get_collect_week_schedule(cls):
                return MessagesTemplates.messages_manager.get_message("controller.success.collect_week_schedule")
            
            @classmethod
            def get_collect_raw_week_schedule(cls):
                return MessagesTemplates.messages_manager.get_message("controller.success.collect_raw_week_schedule")
        
        class DBError:

            @classmethod
            def get_collect_all(cls, model, err):
                return MessagesTemplates.messages_manager.get_message("controller.db_error.collect_all", {"model": model, "err": err})
            
            @classmethod
            def get_collect_all_detailed_message(cls, model, err):
                return MessagesTemplates.messages_manager.get_message("controller.db_error.collect_all_detailed", {"model": model, "err": err})
            
            @classmethod
            def get_find_by_id_message(cls, model, err):
                return MessagesTemplates.messages_manager.get_message("controller.db_error.find_by_id", {"model": model, "err": err})
            
            @classmethod
            def get_create_message(cls, model, err):
                return MessagesTemplates.messages_manager.get_message("controller.db_error.create", {"model": model, "err": err})
            
            @classmethod
            def get_update_message(cls, model, err):
                return MessagesTemplates.messages_manager.get_message("controller.db_error.update", {"model": model, "err": err})
            
            @classmethod
            def get_delete_message(cls, model, err):
                return MessagesTemplates.messages_manager.get_message("controller.db_error.delete", {"model": model, "err": err})
            
        class Error:

            @classmethod
            def get_collect_all(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.error.collect_all", {"model": model})
            
            @classmethod
            def get_collect_all_detailed_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.error.collect_all_detailed", {"model": model})
            
            @classmethod
            def get_collect_all_by_model_message(cls, model, filter):
                return MessagesTemplates.messages_manager.get_message("controller.error.collect_all_by_model", {"model": model, "filter": filter})
            
            @classmethod
            def get_find_by_id_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.error.find_by_id", {"model": model})
            
            @classmethod
            def get_find_by_day_and_student_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.error.find_by_day_and_student", {"model": model})
            
            @classmethod
            def get_find_current_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.error.find_current", {"model": model})

            @classmethod
            def get_create_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.error.create", {"model": model})
            
            @classmethod
            def get_update_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.error.update", {"model": model})
            
            @classmethod
            def get_delete_message(cls, model):
                return MessagesTemplates.messages_manager.get_message("controller.error.delete", {"model": model})
            
            @classmethod
            def get_upload_files_message(cls):
                return MessagesTemplates.messages_manager.get_message("controller.error.upload_files")
            